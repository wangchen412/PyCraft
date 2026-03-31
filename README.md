# Settings in Minecraft
  - Settings > General
    - Websockets Enabled -> On
    - Require Encrypted Websockets -> Off
   
# Example
  1. In a Jupyter notebook, ```mlc = MinecraftLiveController.StartServer()```.
  2. Run Minecraft. Enter "/connect 127.0.0.1:6464". Minecraft: Connection established to server: ...".
  3. In another cell of the notebook, use mlc.set_blocks_relative to build blocks at given points.
