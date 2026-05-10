
extends CharacterBody3D
var speed = 5.0
var mechanic_available = true
var mechanic_cooldown = 0.0

func _ready():
    print("Eclipse Ghost – roguelite")
    print("Mechanic: Nightmare Fuel")
    print("Description: enemies see their worst fear and flee")

func _physics_process(delta):
    # Basic movement
    var input = Input.get_vector("left", "right", "forward", "back")
    var dir = (transform.basis * Vector3(input.x, 0, input.y)).normalized()
    velocity.x = dir.x * speed
    velocity.z = dir.z * speed
    move_and_slide()
    
    # Mechanic cooldown
    if mechanic_cooldown > 0:
        mechanic_cooldown -= delta

func use_mechanic():
    if mechanic_available and mechanic_cooldown <= 0:
        print("Nightmare Fuel activated!")
        mechanic_cooldown = 2.0
        return True
    return False
