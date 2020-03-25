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
#define PI_number 3.14159265358979323846  /* pi */

#define ambient_light_coeff 0.2
#define k_d 0.5
#define k_s 0.1
#define n_s 100
#define cos_phi 0.939 /* apr 20 degrees */

class Vector;
class Sphere;
class Color;
bool is_this_closer(Vector& closest_yet, Vector& candidate, const Vector& base_point);

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
    Color operator + (const Color& c) {
        double r = R + c.R;
        double g = G + c.G;
        double b = B + c.B;

        if (r > 255) {r = 255;} else if(r < 0){ r = 0;}
        if (g > 255) {g = 255;} else if(g < 0){ g = 0;}
        if (b > 255) {b = 255;} else if(b < 0){ b = 0;}

    
        return Color(int(r),int(g),int(b));
        
    }

    void operator += (const Color& c) {
        double r = R + c.R;
        double g = G + c.G;
        double b = B + c.B;

        if (r > 255) {r = 255;} else if(r < 0){ r = 0;}
        if (g > 255) {g = 255;} else if(g < 0){ g = 0;}
        if (b > 255) {b = 255;} else if(b < 0){ b = 0;}

        this->R = int(r);
        this->G = int(g);
        this->B = int(b);
    }

    void print_summary() const {
        printf("(R,G,B) : (%d, %d, %d)\n", R, G, B);
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

    return true;
}


bool is_this_closer(Vector& closest_yet, Vector& candidate, const Vector& base_point){

    if((candidate - base_point).length_square() < (closest_yet - base_point).length_square() ){
        return true;
    }else{
        return false;
    }

}


float calculate_light_coeff(Vector& inters_point, Vector& light_source_point, Vector& sphere_center){       

    Vector normal = (inters_point - sphere_center).getNormalized();
    Vector ray_to_light = (light_source_point - inters_point).getNormalized();

    //since both normal and incoming ray are unit vectors the dot product is equal to cosine
    float cosine = normal.dotProduct(ray_to_light); 

    return k_d * cosine + k_s * pow(cos_phi, n_s) ;
}



/**
 * 
 * Trace color of one pixel
 * */
Color trace_pixel_color(Vector &eye, Vector &pixel_point, std::vector<Sphere> &spheres_list, std::vector<Vector> &light_source_points){

    Vector intial_ray = (pixel_point - eye + Vector(0.5,0.5,0.5));//.getNormalized() ; ///the ray starting from eye and going through THE CENTER of this pixel.

    // Vector light_source_point = light_source_points[0];
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

    // bool is_shadowed = false; //true;
    float light_coeff = 0; 

    
    Color light = Color(0,0,0);

    /// now we find out if this point is shed light onto it
    for(std::size_t i = 0; i < light_source_points.size(); i++){
        bool no_shadow = true;
        for(std::size_t j = 0; j < spheres_list.size(); j++){
            Vector ray_to_light = (light_source_points[i] - closest_inters_point);
            if(found_one){
                if(does_intersect(ray_to_light, closest_inters_point, spheres_list[j], point1, point2)){
                   if(closest_inters_point != point2 && is_this_closer(light_source_points[i], point1, closest_inters_point)){
                        no_shadow = false;
                    } 
                }     

            }
        }

        if(found_one && no_shadow){
            light_coeff = calculate_light_coeff(closest_inters_point, light_source_points[i], spheres_list[sphereIndex].center);
            light += Color(255,255,255) * 1.8 * light_coeff; 

        }
         

    }

    if(found_one){
        return spheres_list[sphereIndex].color * ambient_light_coeff + light;

    }

    return Color(255,255,255); ///if can not find any thing return white

}


