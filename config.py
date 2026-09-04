import os

ICON_DIR = "/usr/share/icons/Papirus/128x128/apps"
SCORE_FILE = os.path.expanduser("~/.concentration_scores.enc")
SECRET_KEY_FILE = os.path.expanduser("~/.concentration.key")

ROWS = 4
COLS = 6
TOTAL_CARDS = ROWS * COLS  # 24
TOTAL_MATCHES = TOTAL_CARDS // 2  # 12
GAME_TIME = 300  # 5 minutes countdown
FLIP_TIMEOUT = 3  # Seconds cards stay visible before flipping back or disappearing

# 185 Corrected Icons
AVAILABLE_ICONS = [
    "0ad.svg", "abe.svg", "a-boy-and-his-blob.svg", "afl.svg", "age-of-empires-2.svg",
    "airstrike.svg", "alan-wake.svg", "albion-online.svg", "alien-arena.svg", "alienblaster.svg",
    "alienfx.svg", "annas-quest.svg", "aranym.svg", "armitage.svg", "badland.svg",
    "bastion.svg", "beyond-a-steel-sky.svg", "billard-gl.svg", "blastem.svg", "blinken.svg",
    "blobwars.svg", "boswars.svg", "bugdom.svg", "bzflag.svg", "caveexpress-icon.svg",
    "cave-story.svg", "celeste.svg", "chess.svg", "chocolate-doom.svg", "cities-skylines.svg",
    "crab-game.svg", "crawl.svg", "crusader-kings-2.svg", "crypt-of-the-necrodancer.svg", "cs.svg",
    "cuphead.svg", "day-of-the-tentacle-remastered.svg", "dead-cells.svg", "desmume.svg", "desura.svg",
    "dino.svg", "dont-starve-together.svg", "doom-eternal.svg", "dota2.svg", "dragon-ball-online-global.svg",
    "endless-sky.svg", "enter-the-gungeon.svg", "epiphany-game.svg", "eternallands.svg", "evtest-qt.svg",
    "exult.svg", "fceux.svg", "fheroes2.svg", "foobillardplus.svg", "football.svg",
    "for-the-king.svg", "freeciv-client.svg", "freedroid.svg", "freedroidrpg.svg", "frogatto.svg",
    "frozen-bubble.svg", "funkin.svg", "gcompris.svg", "geotranz.svg", "gnome-chess.svg",
    "gnome-robots.svg", "gnome-sudoku.svg", "gns3.svg", "gnubg.svg", "granatier.svg",
    "grim-fandango-remastered.svg", "half-life.svg", "hedgewars.svg", "helltaker.svg", "hollow-knight.svg",
    "hoppscotch.svg", "hypnospace-outlaw.svg", "i2pd.svg", "ibus-typing-booster.svg", "indivisible.svg",
    "jmonkeyengine.svg", "kapman.svg", "kasteroids.svg", "kawanime.svg", "kerbal-space-program.svg",
    "kwybase.svg", "kgeography.svg", "kitty.svg", "kmahjongg.svg", "knavalbattle.svg",
    "koala.svg", "knights-game.svg", "konquest.svg", "kspaceduel.svg", "kturtle.svg",
    "league-of-legends.svg", "lightzone.svg", "limbo.svg", "little-inferno.svg", "lovely-planet-2.svg",
    "lutris.svg", "machinarium.svg", "magicka-2.svg", "magictree.svg", "makagiga.svg",
    "mame.svg", "manaplus.svg", "matlab.svg", "mcpelauncher-ui-qt.svg", "mednafen.svg",
    "meow.svg", "meshlab.svg", "minecraft.svg", "minigalaxy.svg", "mrboom.svg",
    "nekopara.svg", "neverball.svg", "nexuiz.svg", "night-in-the-woods.svg", "nutstore.svg",
    "octodad-dadliest-catch.svg", "octopi.svg", "oolite.svg", "openclonk.svg", "opentyrian.svg",
    "openxcom.svg", "oxygen-not-included.svg", "papagayong.svg", "pekka-kana-2.svg", "peruse.svg",
    "phantompeer.svg", "pingus.svg", "pixel-piracy.svg", "playonlinux.svg", "pokerth.svg",
    "popcorn-time.svg", "powermanga.svg", "pr-boom-plus.svg", "quake3.svg", "rememberthemilk.svg",
    "renpy.svg", "restic.svg", "retroarch.svg", "retropie.svg", "rogue-legacy.svg",
    "rpg-maker-mv.svg", "sakura-dungeon.svg", "sauerbraten.svg", "scratch.svg", "scummvm.svg",
    "skullgirls.svg", "slay-the-spire.svg", "slime-rancher.svg", "smc.svg", "smokinguns.svg",
    "smw.svg", "solarus.svg", "soma.svg", "space-engineers.svg", "sparrow.svg",
    "spek.svg", "stardew-valley.svg", "stealth-bastard.deluxe.svg", "steam.svg", "stella.svg",
    "subsurface-icon.svg", "supertux.svg", "supertuxkart.svg", "teeworlds.svg", "teslagrad.svg",
    "the-binding-of-isaac-rebirth.svg", "textosaurus.svg", "the-cave.svg", "the-escapists-2.svg", "the-swapper.svg",
    "the-witcher.svg", "tibia.svg", "toki-tori.svg", "trine3.svg", "tsc.svg",
    "turtleart.svg", "vita3k.svg", "warmux.svg", "worms-armageddon.svg", "xmoto.svg"
]
