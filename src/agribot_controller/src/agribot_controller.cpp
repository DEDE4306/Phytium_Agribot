#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>
#include <nav_msgs/msg/odometry.hpp>

using namespace rclcpp;
using std::placeholders::_1;

class AgribotController: public Node{
public:
    AgribotController(): Node("agribot_controller"), 
    obstacle_distance_threshold_(0.5),
    obstacle_detected_(false){
        laser_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 10, std::bind(&AgribotController::laser_callback, _1)
        );
        odom_sub_ = this->create_subscription<nav_msgs::msg::Odometry>(
            "/odom", 10, std::bind(&AgribotController::odom_callback, _1)
        );
        cmd_vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>(
            "/cmd_vel", 10
        );
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&AgribotController::control_loop, this)
        );
    }

    void laser_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg){
        obstacle_detected_= false;
        for (auto range: msg->ranges) {
            if(range < obstacle_distance_threshold_) {
                obstacle_detected_ = true;
                break;
            }
        }
    }

    void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg){
        return;
        // 获取机器人位姿或速度，后续开发可能用到
    }

    void control_loop(){
        if(obstacle_detected_) {
            RCLCPP_INFO(this->get_logger(),"遇到障碍物，开始避障");
            // 避障，停下后原地旋转
            current_cmd_.linear.x = 0.0;
            current_cmd_.angular.z = 0.5;   // 原地旋转 
        }
        else {
            RCLCPP_INFO(this->get_logger(),"正常前进");
            // 正常前进
            current_cmd_.linear.x = 0.2;
            current_cmd_.angular.z = 0.0;
        }
        cmd_vel_pub_->publish(current_cmd_);
    }
private:
    // 订阅雷达和里程计信息
    Subscription<sensor_msgs::msg::LaserScan>::SharedPtr laser_sub_;
    Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
    // 发布速度信息
    Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
    // 计时器
    TimerBase::SharedPtr timer_;
    //
    geometry_msgs::msg::Twist current_cmd_;
    // 避障相关参数
    float obstacle_distance_threshold_;
    bool obstacle_detected_;
};

int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AgribotController>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}