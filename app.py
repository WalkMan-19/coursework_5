from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from base import Arena
from classes import unit_classes
from unit import BaseUnit, PlayerUnit, EnemyUnit
from equipment import Equipment

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == 'GET':
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        result = {
            'header': 'Выберете героя',
            'classes': classes,
            'weapons': weapons,
            'armors': armors,
        }
        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        name = request.form.get("name")
        armor_name = request.form.get("armor")
        weapon_name = request.form.get("weapon")
        unit_class = request.form.get("unit_class")
        player = PlayerUnit(
            name=name,
            unit_class=unit_classes[unit_class],
        )
        equipment = Equipment()
        player.equip_armor(equipment.get_armor(armor_name))
        player.equip_weapon(equipment.get_weapon(weapon_name))
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == 'GET':
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        result = {
            'header': 'Выберете противника',
            'classes': classes,
            'weapons': weapons,
            'armors': armors,
        }
        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        name = request.form.get("name")
        armor_name = request.form.get("armor")
        weapon_name = request.form.get("weapon")
        unit_class = request.form.get("unit_class")
        enemy = EnemyUnit(
            name=name,
            unit_class=unit_classes[unit_class],
        )
        equipment = Equipment()
        enemy.equip_armor(equipment.get_armor(armor_name))
        enemy.equip_weapon(equipment.get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
