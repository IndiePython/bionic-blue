# Bionic Blue (by Kennedy Guerra)

<img style="display:block;margin:auto;" alt="game logo" src="https://i.imgur.com/tjBQKXp.png" />
<br />

<img style="display:block;margin:auto;" alt="game screenshot" src="https://i.imgur.com/wtGpzXK.png" />
<br />

<img style="display:block;margin:auto;" alt="game screenshot" src="https://i.imgur.com/kfKJRTD.gif" />
<br />


Bionic Blue is an action platformer game featuring a bionic boy tasked with protecting humanity against dangerous robots. It is currently at an early stage of development and for now works like a demo to showcase gameplay. This project is part of the [Indie Python](https://github.com/IndiePython) project and has a [dedicated website](https://bionicblue.indiepython.com) where you can find more info about it.

It is made in [Python](https://github.com/python/cpython)/[pygame-ce](https://github.com/pygame-community/pygame-ce) targeting desktop platforms where Python is available like Windows, Mac and Linux.

This game was created by [Kennedy R. S. Guerra](https://kennedyrichard.com) (me), who also develops/maintains the game.

Check this youtube video where the game is briefly presented:

<a href="https://www.youtube.com/watch?v=oTrZM4GC_3w">
  <img style="display:block;margin:auto;" alt="thumb of youtube video" src="https://img.youtube.com/vi/oTrZM4GC_3w/hqdefault.jpg" />
</a>

<br />


## Installing & running the game

To run the game, installation is actually optional.


### If you want to install...

You can install bionic blue from the Python Package Index with the `pip` command:

```bash
pip install bionicblue
```

This will install the `pygame-ce` library (pygame community edition fork) as well if not already present. To run the installed game, all you need now is to run the `bionicblue` command.


### If you want to use as a standalone program

Download the `bionicblue` folder in the top of the repository folder. Then, if you have the `pygame-ce` library (pygame community edition fork) installed in the Python instance you'll use to run the game, you just need to execute the command below in the directory where you put the `bionicblue` folder:

```python
python3 -m bionicblue
```

Depending on your system, you might need to use the `python` command instead of the `python3` command above. That's all you should need.

However, if the pygame installed in the Python instance used to run the game isn't pygame-ce the game won't launch. Instead, a dialog will appear explaining the problem and providing instructions to replace your pygame installation by the community edition fork. Both regular pygame and the community edition fork (pygame-ce) are great, but the game can only run with pygame-ce because it uses services that are available solely in that library.


## Controls

The controls are configurable both for keyboard and gamepad.

Default controls for keyboard are...

| Action | Key |
| --- | --- |
| Movement | w, a, s, d keys |
| Shoot | j |
| Jump | k |

Enter (return) and escape keys are reserved for confirming and exitting/going back, respectively. Arrow keys are used to navigate menus, but can also be configured to be used for moving the character.

Regarding the gamepad, the user doesn't need to configure directional buttons/triggers. Those are detected and managed automatically. The user only needs to configure the gamepad for actions like shooting, jumping, etc.



## Contributing

Keep in mind this is a game project, so it has a design and finite set of features defined by its creator (me, Kennedy Guerra) according to his vision. In other words, as much as we love contributions in general in the Indie Python project, for this game project we would like the contributions to be limited to refactoring/optimizing/fixing the existing code, rather than changing the design/content of the game.

If in doubt, please [start a discussion](https://github.com/IndiePython/bionic-blue/discussions) first, in order to discuss what you would like to change.


## Issues

Issues are reserved for things that crash the game or otherwise prevent the user from progressing in the game. Please, if you're not certain, [start a discussion](https://github.com/IndiePython/bionic-blue/discussions) instead. It can always be converted into an issue later if needed.

## Contact

Contact me any time via [twitter](https://twitter.com/KennedyRichard), [mastodon](https://fosstodon.org/KennedyRichard) or [email](mailto:kennedy@kennedyrichard.com).

You are also welcome on the Indie Python's [discord server](https://indiepython.com/discord).


## License

Bionic Blue is dedicated to the public domain with [The Unlicense](https://unlicense.org/).


## Help the Indie Python project

Please, [support the Indie Python project](https://indiepython.com/donate) so more free open-source games like this one can be made.


## Why the name on game's title

Making games is arduous and honest work. Musicians, illustrators and many other professionals always sign their works. People who make games should not be afraid of doing so as well. Check [Bennett Foddy and Zach Gage's video](https://www.youtube.com/watch?v=N4UFC0y1tY0) to learn more about this.
