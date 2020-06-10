from app import app
from app.robots import robot_runner

if __name__ == "__main__":
    #robots = robot_runner.robot_runner()  
    #robots.threadRun()
    app.run("0.0.0.0", 5000, debug=True)
