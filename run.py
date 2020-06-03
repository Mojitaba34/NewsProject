from app import app
from app.robots import robot_runner
if __name__ == "__main__":
    """robot_runner.tejarat_test()
    robot_runner.arzdigital_test()
    robot_runner.tasnim_test()"""
    app.run("0.0.0.0", 5000, debug=True)
