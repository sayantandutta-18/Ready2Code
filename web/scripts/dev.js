const net = require("net");
const { spawn } = require("child_process");

const PORT = parseInt(process.env.PORT || "3000", 10);

function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    server.once("error", (err) => {
      if (err.code === "EADDRINUSE") {
        resolve(false);
      } else {
        resolve(true);
      }
    });
    server.once("listening", () => {
      server.close(() => resolve(true));
    });
    server.listen(port);
  });
}

async function main() {
  const isAvailable = await checkPort(PORT);
  if (!isAvailable) {
    console.error(`\n[Ready2Code] ERROR: Port ${PORT} is currently busy / in use by another process.`);
    console.error(`Ready2Code web server requires port ${PORT} by default.`);
    console.error(`Please free port ${PORT} or set PORT=<port> npm run dev.\n`);
    process.exit(1);
  }

  const isWindows = process.platform === "win32";
  const cmd = isWindows ? "npx.cmd" : "npx";
  const child = spawn(cmd, ["next", "dev", "-p", String(PORT)], {
    stdio: "inherit",
    env: process.env,
    shell: isWindows,
  });

  child.on("exit", (code) => {
    process.exit(code || 0);
  });
}

main();
