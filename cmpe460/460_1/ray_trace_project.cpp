#include <iostream>
#include <stdio.h>
#include <cmath>
#include <stdexcept>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <stdlib.h>

#define TOO_FAR 1e4
#define epsilon 1e-6


class Vector;
class Sphere;
class Color;
bool is_this_closer(Vector& closest_yet, Vector& candidate, const Vector& the_eye);

/**
    This class is used to represent Rays AND points
*/
class Vector
{
public:
    double x, y, z;
    Vector(double x, double y, double z):x(x),y(y),z(z){ /* Empty */}

    /*redefine common operators*/
    Vector operator - (const Vector &v) const { return Vector(x - v.x, y - v.y, z - v.z); }
    Vector operator + (const Vector &v) const { return Vector(x + v.x, y + v.y, z + v.z); }

    Vector operator * (const Vector &v) const { return Vector(x * v.x, y * v.y, z * v.z); }

    bool operator == (const Vector &v) const { return (std::abs(x - v.x) < epsilon && std::abs(y - v.y) < epsilon && std::abs(z - v.z) < epsilon); }
    bool operator != (const Vector &v) const { return (std::abs(x - v.x) >= epsilon || std::abs(y - v.y) >= epsilon || std::abs(z - v.z) >= epsilon); }


    Vector& operator += (const Vector &v) { x += v.x, y += v.y, z += v.z; return *this; }
    Vector& operator *= (const Vector &v) { x *= v.x, y *= v.y, z *= v.z; return *this; }

    double length_square() const { return x * x + y * y + z * z; }
    double length_() const { return sqrt(length_square()); }

    double dotProduct(const Vector& v) const {
        // printf("debugging dotProduct\n" );
        // print_summary();
        // v.print_summary();

        // printf("x * v.x %f\n",  x * v.x);
        // printf("y * v.y %f\n",  y * v.y);
        // printf("z * v.z %f\n",  z * v.z);
        //
        // printf("x * v.x + y * v.y + z * v.z %f\n",  x * v.x + y * v.y + z * v.z);
        return x * v.x + y * v.y + z * v.z;

    }

    void setZero(){
        x = 0;
        y = 0;
        z = 0;
    }

    void set_TOO_FAR() {
        x = TOO_FAR;
        y = TOO_FAR;
        z = TOO_FAR;
    }


    const Vector getNormalized() const
    {

        if(x == 0 && y == 0 && z == 0){
            throw std::invalid_argument( "This is a zero vector thus can not be normalized" );
        }

        double length = length_();

        return Vector(x/length, y/length, z/length);
    }

    void print_summary() const {
        printf("(x,y,z) : (%f, %f, %f)\n",x, y, z);
    };

};


class Color
{
public:
    int R, G, B;

    Color(int R, int G, int B): R(R), G(G), B(B){ /* Empty */ }

    Color operator * (double coeff) {return Color(R * coeff, G * coeff, B * coeff); }

    void print_summary() const {
        printf("(R,G,B) : (%d, %d, %d)\n",R, G, B);
    };

};

class Sphere
{
public:
    Vector center ;                            //the center
    double r ;                            // radius
    Color color ;

    Sphere(
        const Vector &center,
        const double &r,
        const Color &color) :
        center(center), r(r), color(color)
    { /* empty */ }

    void print_summary() const {
        printf("Sphere : \n");
        printf("r = %f\ncenter = ", r);
        center.print_summary();
        color.print_summary();
    }



};


/**
    Checks is given line and sphere intersect, returns true if they do.
    Also intersection `points` point1 and point2 are modified so that they can be used from the caller
    Note that Vector objects are used as points here.

*/
bool does_intersect(const Vector &vec, const Vector &ray_origin, const Sphere &sp, Vector &point1, Vector &point2){
    // Vector l = sp.center - rayorig;
    Vector normalizedVec = vec.getNormalized();
    ///shift the sphere so that the origin of the ray is at (0,0,0)
    /// all the computations are based on this shifted 3D space
    /// the intersection points are shifted back at the and
    Vector shifted_shpere = sp.center - ray_origin; ///we will continue with this shifted sphrere (sphere center)

    double tca = shifted_shpere.dotProduct(normalizedVec);
    if (tca < 0) return false;

    ///d2 (d^2) is the square of the distance between the center of the sphere and the direction line of the `ray`(Vector vec)
    double d2 = shifted_shpere.length_square() - pow(tca,2);
    // printf("d2 %f\n", d2);

    ///the square of the radious a.k.a : r^2
    double r_square = pow(sp.r,2);
    // printf("r_square %f\n", r_square);


    /// if the distance (see above description of d2) is larger than r^2 than the line never is completely outside of the spheres
    if (d2 > r_square) return false;


    // printf("d2 %f\n", d2);
    // printf("r_square %f\n", r_square);



    /// hard to describe but... 2*thc correspounds to the length of the line segment that is inside the sphere.
    /// if you draw it on paper you wll see it. we are only doing pisagor here. Nothing too fancy.
    double thc = sqrt(r_square - d2);
    // printf("thc %f\n", thc);


    ///the distance from origin to the closer intersection point
    double t0 = tca - thc;
    // printf("t0 %f\n", t0);


    ///the distance from origin to the farther intersection point
    double t1 = tca + thc;
    // printf("t1 %f\n", t1);


    if (t0 > t1) std::swap(t0, t1); //we want t0 to be small one



    if(std::abs(int(t0)) == 0 && t1 < 0){
         return false;
    }

    if (t0<0){
        t0 = t1;
        if (t0 < 0) return false; // both t0 and t1 are negative
    }


    ///set the intersection `points`
    point1.setZero();
    point1 += Vector(normalizedVec.x * t0 ,normalizedVec.y * t0 , normalizedVec.z * t0 ) + ray_origin; /// + ray_origin is the shift back

    point2.setZero();
    point2 += Vector(normalizedVec.x * t1  ,normalizedVec.y * t1  , normalizedVec.z * t1 ) + ray_origin; /// + ray_origin is the shift back




    // if(is_this_closer(point1, point2, ray_origin)){
    //     printf("point2 < point1\n" );
    // }

    return true;
}


bool is_this_closer(Vector& closest_yet, Vector& candidate, const Vector& the_eye){

    if((candidate - the_eye).length_square() < (closest_yet - the_eye).length_square() ){
        return true;
    }else{
        return false;
    }

}

Color trace_pixel_color(Vector &eye, Vector &pixel_point, std::vector<Sphere> &spheres_list, Vector &light_source_point){

    Vector intial_ray = (pixel_point - eye + Vector(0.5,0.5,0.5));//.getNormalized() ; ///the ray starting from eye and going through THE CENTER of this pixel.
    Vector ray_to_light = Vector(0,0,0);

    Vector closest_inters_point = Vector(TOO_FAR, TOO_FAR, TOO_FAR);
    Vector point1 = Vector(TOO_FAR,TOO_FAR,TOO_FAR);
    Vector point2 = Vector(TOO_FAR,TOO_FAR,TOO_FAR);

    bool found_one = false;
    unsigned int sphereIndex = -1;

    /// we find the closest of the intersection points
    for(std::size_t i = 0; i < spheres_list.size(); i++){

        //point1 and point2 are modified to be intersection points in the function --->
        if(does_intersect(intial_ray, eye, spheres_list[i], point1, point2)){  //  --> only if the function is to return true
            found_one = true;


            if(is_this_closer(closest_inters_point, point1, eye)){
                closest_inters_point = point1;
                sphereIndex = i;
            }


        }

    }

    point1.set_TOO_FAR();
    point2.set_TOO_FAR();

    bool is_shadowed = false;

    /// now we find out if this point is shed light onto it
    if(found_one){
        ray_to_light = (light_source_point - closest_inters_point);//.getNormalized();
        // ray_to_light.print_summary();

        for(std::size_t i = 0; i < spheres_list.size(); i++){

            //point1 and point2 are modified to be intersection points in the function --->
            if(does_intersect(ray_to_light, closest_inters_point, spheres_list[i], point1, point2)){  //  --> only if the function is to return true
                if(closest_inters_point != point2){
                    is_shadowed = true;
                }
                // point1.print_summary();
                // point2.print_summary();

                // printf(" %d\n", closest_inters_point == point1);
            }

        }

        if(is_shadowed){
            return spheres_list[sphereIndex].color * (0.5);

        }else{
            return spheres_list[sphereIndex].color;

        }

    }

    return Color(255,255,255); ///if can not find any thing return white

}


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



    // for (std::vector<Sphere>::const_iterator i = spheres_list.begin(); i != spheres_list.end(); ++i)
    //     i->print_summary();

    ///input ended


    //
    // Sphere sphere1 = Sphere(Vector(50,50,300), 100.0, Color(255,0,0));
    //
    // Sphere sphere2 = Sphere(Vector(-1000,100,600), 300.0, Color(0,255,0));


    Vector eye = Vector(0,0,0);

    // std::vector<Sphere> spheres_list;


    // spheres_list.push_back(sphere1);
    //
    // spheres_list.push_back(sphere2);


    Vector light_source_point = Vector(500, 500, 500);

    Vector pixel_point = Vector(0,0,0); /// values are not important

    Color answer = Color(255,255,255); //trace_pixel_color(eye, pixel_point , spheres_list, light_source_point);

    // answer.print_summary();


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
    // printf("P6 1000 1000 255 "); // PPM header
    for(double y = 50; y > -50; y-=0.1){  //to be 100 to 100 , i ignore 50  z = 100 is fixed
        for(double x = -50; x < 50 ; x+=0.1){
            pixel_point.x = x;
            pixel_point.y = y;
            pixel_point.z = 100;
            answer = trace_pixel_color(eye, pixel_point , spheres_list, light_source_point);
            outputFile << (char)answer.R << (char)answer.G << (char)answer.B;
            // printf("%c%c%c", (int)answer.R, (int)answer.G, (int)answer.B);
        }
    }


return 0;
}
