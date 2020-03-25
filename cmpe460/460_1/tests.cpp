void unittest_does_intersect(){
    Sphere sphere = Sphere(Vector(400,400,400), 100.0, Color(255,0,0));
    Vector ray = Vector(1,1,1);

    Vector point1 = Vector(0,0,0);
    Vector point2 = Vector(0,0,0);

    Vector origin_of_Ray = Vector(0,0,0);

    if(does_intersect(ray,origin_of_Ray,sphere,point1,point2)){
        point1.print_summary();
        point2.print_summary();

    }
    //Expected :
    //(x,y,z) : (342.264973, 342.264973, 342.264973)
    //(x,y,z) : (457.735027, 457.735027, 457.735027)

}


void test2(){




    Sphere sphere = Sphere(Vector(400,400,400), 100.0, Color(255,0,0));


    Vector eye = Vector(0,0,0);

    std::vector<Sphere> spheres_list;
    spheres_list.push_back(sphere);

    Vector light_source_point = Vector(600,600,600);

    Vector pixel_point = Vector(2,2,2);

    Color answer = trace_pixel_color(eye, pixel_point , spheres_list, light_source_point);

    answer.print_summary();
}


int main(int argc, char **argv)
{


    //
    Sphere sphere1 = Sphere(Vector(-30,-30,300), 10.0, Color(255,0,0));

    Sphere sphere2 = Sphere(Vector(70,70,300), 90.0, Color(0,255,0));


    Vector eye = Vector(0,0,0);

    std::vector<Sphere> spheres_list;
    spheres_list.push_back(sphere1);

    spheres_list.push_back(sphere2);


    Vector light_source_point = Vector(-60,-60,300);

    Vector pixel_point = Vector(2,2,3); /// values are not important

    Color answer = trace_pixel_color(eye, pixel_point , spheres_list, light_source_point);

    // answer.print_summary();



    printf("P6 100 100 255 "); // PPM header
    for(int y = 50; y > -50; y--){  //to be 100 to 100 , i ignore 50  z = 100 is fixed
        for(int x = -50; x < 50 ; x++){
            pixel_point.x = x;
            pixel_point.y = y;
            pixel_point.z = 100;
            answer = trace_pixel_color(eye, pixel_point , spheres_list, light_source_point);
            printf("%c%c%c", (int)answer.R, (int)answer.G, (int)answer.B);
            // std::cout << (int)answer.R << (int)answer.G <<  (int)answer.B ;
        }
    }


return 0;
}



int main(int argc, char **argv)
{


    //
    Sphere sphere1 = Sphere(Vector(50,50,300), 20.0, Color(255,0,0));

    Sphere sphere2 = Sphere(Vector(100,100,600), 60.0, Color(0,255,0));


    Vector eye = Vector(0,0,0);

    std::vector<Sphere> spheres_list;
    spheres_list.push_back(sphere1);

    spheres_list.push_back(sphere2);


    Vector light_source_point = Vector(500,500,500);

    Vector pixel_point = Vector(2,2,3); /// values are not important

    Color answer = trace_pixel_color(eye, pixel_point , spheres_list, light_source_point);

    // answer.print_summary();



    printf("P6 1000 1000 255 "); // PPM header
    for(int y = 500; y > -500; y--){  //to be 100 to 100 , i ignore 50  z = 100 is fixed
        for(int x = -500; x < 500 ; x++){
            pixel_point.x = x;
            pixel_point.y = y;
            pixel_point.z = 100;
            answer = trace_pixel_color(eye, pixel_point , spheres_list, light_source_point);
            printf("%c%c%c", (int)answer.R, (int)answer.G, (int)answer.B);
            // std::cout << (int)answer.R << (int)answer.G <<  (int)answer.B ;
        }
    }


return 0;
}



for (std::vector<Vector>::const_iterator i = centers.begin(); i != centers.end(); ++i)
    i->print_summary();

for (std::vector<double>::const_iterator i = radius_list.begin(); i != radius_list.end(); ++i)
    std::cout << *i << "\n";

for (std::vector<Color>::const_iterator i = colors.begin(); i != colors.end(); ++i)
    i->print_summary();
