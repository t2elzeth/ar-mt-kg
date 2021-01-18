const http = require("http");
const express = require("express");
const socketio = require("socket.io")

const app = express();
const server = http.createServer(app)
const io = socketio(server);
const PORT = 8920

io.on("connection", socket => {
  console.log("Successfully connected!");

  socket.on("new-project", () => {
  })

  socket.on("no-projects", () => {
  })

  socket.on("disconnect", () => console.log("Client has been disconnected!"))
})

server.listen(PORT, () => console.log("Server is listening..."))