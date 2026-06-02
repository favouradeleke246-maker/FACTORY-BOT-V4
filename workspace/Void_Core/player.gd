
extends CharacterBody2D
var speed = 300
func _ready():
    print("Void Core - top-down shooter")
    print("Mechanic: Mirror Shell")
func _physics_process(delta):
    var input = Vector2(
        Input.get_axis("left", "right"),
        Input.get_axis("up", "down")
    )
    velocity = input * speed
    move_and_slide()
