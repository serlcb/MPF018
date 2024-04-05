#include <iostream>

int main()
{
    int i;
    
    std::cin >> i;
    if (i>4) {
        std::cout << i << " é maior que 4\n";
    } else {
        std::cout << i << " é menor ou igual a 4\n";    
    }
    std::cout<<i;
    return 0;
}

