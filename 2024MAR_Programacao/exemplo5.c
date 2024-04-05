#include <iostream>

double fat(double x);

int main()
{
    int i;
    
    do {
        std::cin << i;
        std::cout << "O fatorial de i é " << fat(i) << "\n";
    } while (i>0);
    
    return 0;
}

double fatorial(double x)

{
    double fat;
    fat=1;
    
    while (x>1) {
        fat=fat*x;
        x=x-1;
    }
    return fat;    
}

