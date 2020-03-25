#include <iostream>
#include <stdio.h>
#include <cmath>
#include <stdexcept>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <stdlib.h>
#include "ray_trace_project.cpp"

int main(int argc, char **argv)
{
    ///input
    std::ifstream infile(argv[1]);


    std::string line;

    std::getline(infile, line); ///get first line;

    int number_of_spheres = atoi( line.substr(line.find_last_of( " " ) + 1).c_str() );

    // printf("%d\n", number_of_spheres);


    /// get colors

    std::vector<Color> colors;
    for(int i = number_of_spheres ; i > 0 ; i--){
        std::getline(infile, line);

        int R, G, B;
        std::string temp = line.substr(line.find_last_of( "=" ) + 1).c_str();
        temp = temp.substr(1,temp.length() -1 );

        int first_comma_index = temp.find(",");
        int last_comma_index = temp.find_last_of(",");

        R = atoi( temp.substr(0, first_comma_index).c_str());
        G = atoi( temp.substr(first_comma_index  + 1, last_comma_index).c_str());
        B = atoi( temp.substr(temp.find_last_of( "," ) + 1).c_str() );

        colors.push_back(Color(R,G,B));

        // colors.back().print_summary();
    }

    std::vector<Vector> centers;
    std::vector<double> radius_list;
    for(int i = number_of_spheres ; i > 0 ; i--){

        ///get center position
        std::getline(infile, line);

        double x, y, z;
        std::string temp = line.substr(line.find_last_of( ":" ) + 1).c_str();
        temp = temp.substr(temp.find("(") + 1,temp.find_last_of(")"));

        int first_comma_index = temp.find(",");
        int last_comma_index = temp.find_last_of(",");

        x = atoi( temp.substr(0, first_comma_index).c_str());
        y = atoi( temp.substr(first_comma_index  + 1, last_comma_index).c_str());
        z = atoi( temp.substr(temp.find_last_of( "," ) + 1).c_str() );

        centers.push_back(Vector(x, y, z));

        // centers.back().print_summary();

        ///get radius
        std::getline(infile, line);

        int radius = atoi(line.substr(line.find_last_of("=") + 1).c_str());

        radius_list.push_back(radius);

        // printf("radius = %d\n", radius);
    }

    std::vector<Sphere> spheres_list;
    for(int i = number_of_spheres - 1; i >= 0 ; i--){
        spheres_list.push_back(Sphere(Vector(centers[i].x,centers[i].y,centers[i].z),radius_list[i],Color(colors[i].R,colors[i].G,colors[i].B)));

    }


    std::vector<Vector> light_source_points;

    std::getline(infile, line); // get number of lights

    int number_of_lights = atoi(line.c_str());

    for(int i = number_of_lights ; i > 0 ; i--){
        std::getline(infile, line);

        int first_comma_index = line.find(",");
        int last_comma_index = line.find_last_of(",");

        int x = atoi( line.substr(0, first_comma_index).c_str());
        int y = atoi( line.substr(first_comma_index  + 1, last_comma_index).c_str());
        int z = atoi( line.substr(line.find_last_of( "," ) + 1).c_str() );

        light_source_points.push_back(Vector(x, y, z));

    }
    


    Vector eye = Vector(0,0,0);


    Vector pixel_point = Vector(0,0,0); /// values are not important

    Color answer = Color(255,255,255); //trace_pixel_color(eye, pixel_point , spheres_list, light_source_point);


    /// output
    std::string output_file_name = "";

    std::string::size_type index = std::string(argv[1]).find_last_of(".");
    if(index != std::string::npos){
        output_file_name = std::string(argv[1]).substr(0,index) + "_output.ppm";
    }else{
        output_file_name = std::string(argv[1]) + "_output.ppm";
    }

    std::ofstream outputFile(output_file_name.c_str());
    outputFile << "P6 1000 1000 255 ";
    for(double y = 50; y > -50; y-=0.1){  //to be 1000 to 1000 , i ignore 50  z = 100 is fixed
        for(double x = -50; x < 50 ; x+=0.1){
            pixel_point.x = x;
            pixel_point.y = y;
            pixel_point.z = 100;
            answer = trace_pixel_color(eye, pixel_point , spheres_list, light_source_points);
            outputFile << (char)answer.R << (char)answer.G << (char)answer.B;
            // printf("%c%c%c", (int)answer.R, (int)answer.G, (int)answer.B);
        }
    }


return 0;
}
