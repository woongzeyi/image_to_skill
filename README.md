# image_to_skill

Convert images to MythicMobs skills.

## Build

```
$ poetry install
$ poetry shell
$ pyinstaller cli --name image_to_skill --onefile
```

The executable will be inside `./dist` directory.

## Use

1. Run the executable once to initialize an `images` directory

2. Put your images inside the `images` directory

3. Run again and configure each generation option before generating each image into code

4. Head to `images` directory and you'll see MythicMobs skills as `.yml` lying beside the images

## Meaning

Mode: Available modes are HR (Horizontal) and VT (Vertical), these will change the orientation of the generated skill

Particle type: Available types can be seen [here](https://git.mythiccraft.io/mythiccraft/MythicMobs/-/wikis/skills/effects/particles/types)

Particle interval: The distance between two particles

Particle size: The size of the particles

Base forward offset: The x distance of the skill and the caster

Base side offset: The z distance of the skill and the caster

Base Y offset: The y distance of the skill and the caster

## License

Licensed under the Apache License 2.0
