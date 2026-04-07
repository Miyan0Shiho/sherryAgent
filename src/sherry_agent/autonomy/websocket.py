import asyncio
import json
from typing import Dict, List, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """接受新的 WebSocket 连接"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """断开 WebSocket 连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        """广播消息给所有连接的客户端"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                self.disconnect(connection)


class WebSocketServer:
    """WebSocket 服务器"""

    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.app = FastAPI()
        self.manager = ConnectionManager()
        self._setup_routes()
        self._setup_cors()
        self.server_task: asyncio.Task | None = None

    def _setup_routes(self):
        """设置路由"""
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.manager.connect(websocket)
            try:
                while True:
                    # 接收客户端消息（可选）
                    await websocket.receive_text()
            except WebSocketDisconnect:
                self.manager.disconnect(websocket)

        @self.app.get("/")
        async def root():
            return {"message": "SherryAgent WebSocket Server"}

        @self.app.get("/status")
        async def get_status():
            return {
                "active_connections": len(self.manager.active_connections),
                "server": f"{self.host}:{self.port}"
            }

    def _setup_cors(self):
        """设置 CORS"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # 在生产环境中应该设置具体的域名
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    async def start(self):
        """启动服务器"""
        import uvicorn
        config = uvicorn.Config(self.app, host=self.host, port=self.port)
        server = uvicorn.Server(config)
        await server.serve()

    def start_in_background(self):
        """在后台启动服务器"""
        self.server_task = asyncio.create_task(self.start())

    async def stop(self):
        """停止服务器"""
        if self.server_task:
            self.server_task.cancel()
            try:
                await self.server_task
            except asyncio.CancelledError:
                pass

    async def send_message(self, message: Dict[str, Any]):
        """发送消息给所有客户端"""
        await self.manager.broadcast(message)

    def send_status_update(self, status: Dict[str, Any]):
        """发送状态更新"""
        message = {
            "type": "status_update",
            "data": status,
            "timestamp": asyncio.get_event_loop().time()
        }
        asyncio.create_task(self.send_message(message))
