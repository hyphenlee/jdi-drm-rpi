## build for ColorBerry
build sdl2 at first, like glowfire
```bash
git clone https://github.com/mgba-emu/mgba.git
cd mgba && mkdir build
cd build
cmake ..
make -j4
sudo ./sdl/mgba-qt -f ~/game/Kirby-Mirror.gba
```

## keymap
src/platform/sdl/sdl-events.c
map key to wasd and uijk
```diff
line:142
void mSDLInitBindingsGBA(struct mInputMap* inputMap) {
-       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_x, GBA_KEY_A);
-       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_z, GBA_KEY_B);
-       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_a, GBA_KEY_L);
-       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_s, GBA_KEY_R);
+       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_u, GBA_KEY_A);
+       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_i, GBA_KEY_B);
+       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_j, GBA_KEY_L);
+       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_k, GBA_KEY_R);
        mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_RETURN, GBA_KEY_START);
        mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_BACKSPACE, GBA_KEY_SELECT);
-       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_UP, GBA_KEY_UP);
-       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_DOWN, GBA_KEY_DOWN);
-       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_LEFT, GBA_KEY_LEFT);
-       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_RIGHT, GBA_KEY_RIGHT);
+       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_w, GBA_KEY_UP);
+       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_s, GBA_KEY_DOWN);
+       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_a, GBA_KEY_LEFT);
+       mInputBindKey(inputMap, SDL_BINDING_KEY, SDLK_d, GBA_KEY_RIGHT);

```