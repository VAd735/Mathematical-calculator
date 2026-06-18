
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline #Interpolacja

def get_float_input(prompt):
    """\nFunkcja pomocnicza umożliwiająca bezpieczne wprowadzanie numerów."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("\nBłąd wartości! Prosze wprowadzic wartosc liczbową.")

Bold = '\033[1m'
End = '\033[0m'

"""========================================================================================================================================================"""

def solve_nonlinear():
    print("\n\t--- 1. Równania nieliniowe (Metoda bisekcji) ---")
    print(f" Równanie za domyślnym: {Bold}f(x) = 3 × x² - 4{End}")
    print(" Proces: metoda bisekcji zamienia przedział [a, b] na coraz mniejszy przedział zawierający pierwiastek.")
    print(" Na każdym kroku obliczamy środek przedziału, sprawdzamy znak funkcji i wybieramy podprzedział.")
    
    f = lambda x: 3 * x**2 - 4
    
    a = get_float_input(" Wprowadź początek przedziału (a): ")
    b = get_float_input(" Wprowadź koniec przedziału (b): ")
    e = get_float_input(" Wprowadź dokładność (np. 0.1): ")
    
    if f(a) * f(b) >= 0:
        print(f"\n Błąd: Funkcja musi mieć różne znaki na końcach przedziału {Bold}f({a}) * f({b}) < 0{End}.")
        print(" Oznacza to, że w przedziale musi istnieć przynajmniej jedno miejsce, gdzie funkcja zmienia znak.")
        return
    
    krok = 0
    while (b - a) / 2 > e:
        krok += 1
        xc = (a + b) / 2
        fm = f(xc)
        print(f" Krok {krok}: a = {a:.4f}; b = {b:.4f}; środek = {xc:.4f}; f(a) = {f(a):.4f}; f(b) = {f(b):.4f}; f(mid) = {fm:.4f}")
        
        if fm == 0:
            print("\n Znaleziono dokładny pierwiastek w środku przedziału.")
            break
        elif f(a) * fm < 0:
            print("\n Ponieważ f({a}) i f({xc}) mają przeciwne znaki, rozwiązanie jest w lewym podprzedziale.")
            b = xc
        else:
            print("\n Ponieważ f({xc}) i f({b}) mają przeciwne znaki, rozwiązanie jest w prawym podprzedziale.")
            a = xc
            print(f" Krok {krok}: a = {a:.4f}; b = {b:.4f}; środek = {xc:.4f}; f(a) = {f(a):.4f}; f(b) = {f(b):.4f}; f(mid) = {fm:.4f}")
    print(f"*** Wynik: x ≈ {(a + b) / 2:.4f} ***")

"""========================================================================================================================================================"""

def solve_integration():
    print("\n\t--- 2. Całkowanie numeryczne (Metoda trapezów) ---")
    print(" Wprowadź funkcję w formacie Pythona (np. 3 * x**2 - 4 lub x**3 + 2*x):")
    funkcja = input(" f(x) = ")
    
    f = lambda x: eval(funkcja)
    
    print(f"\n Integracja funkcji: {Bold}f(x) = {funkcja}{End}")
    print(" Proces: przedział [a, b] dzielimy na n trapezów, obliczamy wartość funkcji na końcach każdego trapezu,")
    print(" sumujemy ich pola i mnożymy przez szerokość kroku, aby uzyskać przybliżoną całkę.")
    
    a = get_float_input(" Wprowadź niższą granicę (a): ")
    b = get_float_input(" Wprowadź górną granicę (b): ")
    n = int(get_float_input(" Wprowadź liczbę podziałów (n, liczba całkowita): "))

    h = (b - a) / n
    formula = (f(a) + f(b)) / 2
    
    print(f"\n Integrujemy z krokiem h = {h}")
    print("\n Rozpoczynamy obliczanie sumy wartości funkcji w punktach podziału.")
    suma = 0
    
    for i in range(1, int(n)):
        x = a + i * h
        funkcja = f(x)
        suma += funkcja
        print(f"\n Krok {i}: x = {x:.2f}; f(x) = {funkcja:.2f}; aktualna suma wartości = {suma:.2f}")
        
    wynik = suma * h
    print("\n Po zakończeniu pętli mnożymy sumę przez szerokość kroku, aby otrzymać przybliżoną wartość całki.")
    print(f" *** Wynik: S ≈ {wynik:.4f} *** ")

"""========================================================================================================================================================"""

def solve_linear_systems():
    print("\n\t--- 3. Układy równań liniowych (metoda Gaussa) ---")
    print(" Wybierz rozmiar macierzy:")
    print(" 1. [2×3]")
    print(" 2. [3×3]")
    print(" 3. [4×3]")
    print(" 4. [4×4]")
    print(" 5. [5×3]")
    print(" 6. [5×4]")
    print(" 7. [5×5]")

    choice = input("\n Wybierz rozmiar (1-7): ")
    if choice == '1':
        n, m = 2, 3
    elif choice == '2':
        n, m = 3, 3
    elif choice == '3':
        n, m = 4, 3
    elif choice == '4':
        n, m = 4, 4
    elif choice == '5':
        n, m = 5, 3
    elif choice == '6':
        n, m = 5, 4
    elif choice == '7':
        n, m = 5, 5
    else:
        print("\n Niewłaściwy wybór.")
        return
    
    print(f" Wybrano rozmiar [{n}×{m}]")
    print(" Proces: tworzymy macierz rozszerzoną, normalizujemy wiersze i eliminujemy współczynniki poniżej pivotu.")
    print(" Na koniec wykonujemy podstawianie wsteczne, aby obliczyć wartości zmiennych.")
    
    matrix = []
    for i in range(n):
        row = []
        for j in range(m):
            coeff = get_float_input(f" Równanie {i+1}: wprowadź współczynnik x{j+1}: ")
            row.append(coeff)
        const = get_float_input(f" Równanie {i+1}: wprowadź wolny wyraz: ")
        row.append(const)
        matrix.append(row)

    print(" Początkowa macierz:")
    for row in matrix: print(row)

    for i in range(min(n, m)):
        pivot_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[pivot_row][i]):
                pivot_row = k

        if pivot_row != i:
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            print(f" Zamiana wierszy {i} i {pivot_row}")
        
        pivot = matrix[i][i]
        print(f" Wybieramy pivot w wierszu {i}: {pivot}")
        if abs(pivot) < 1e-10:
            print(" Pivot bliski zero, kontynuacja...")
            continue

        for k in range(i, m + 1):
            matrix[i][k] /= pivot
        print(f" Normalizacja: Wiersz {i} podzielono przez pivot. Nowy wiersz: {matrix[i]}")
        
        for j in range(i + 1, n):
            factor = matrix[j][i]
            print(f" Eliminacja: odejmujemy {factor:.4f} razy wiersz {i} od wiersza {j}.")
            for k in range(i, m + 1):
                matrix[j][k] -= factor * matrix[i][k]
            print(f" Obnulanie: Wiersz {j} zaktualizowany: {matrix[j]}")

    print(" Po eliminacji otrzymujemy macierz w postaci trójkątnej.")
    for row in matrix: print(row)
    
    if n == m:
        x_res = [0 for _ in range(n)]
        for i in range(n - 1, -1, -1):
            x_res[i] = matrix[i][n]
            for k in range(i + 1, n):
                x_res[i] -= matrix[i][k] * x_res[k]
            print(f"\n x{i+1} = {x_res[i]:.4f}")
        print(f"*** Wynik: {', '.join([f'x{i+1} = {x:.4f}' for i, x in enumerate(x_res)])} ***")
    else:
        print("\n System nie jest kwadratowy. Macierz w formie echelonnej powyżej.")

"""========================================================================================================================================================"""

def solve_interpolation():
    print("\n\t--- 4. Interpolacja (Cubic Spline) ---")
    print(" Proces: łączymy podane punkty za pomocą gładkich wielomianów trzeciego stopnia (splajnów).")
    print(" Wykres przejdzie DOKŁADNIE przez każdy wprowadzony punkt.")
    print(" Każdy segment między punktami jest opisany innym wielomianem, ale całość jest gładka (ciągła i ma ciągłą pochodną).")
    
    n = int(get_float_input(" Wprowadź liczbę punktów (minimum 2): "))
    if n < 2:
        print("\n Błąd: Do interpolacji splajnami potrzebne są co najmniej 2 punkty.")
        return
        
    x_pts = []
    y_pts = []
    
    print("\n Podaj współrzędne punktów (można użyć liczb ujemnych, sortuj według rosnącego X):")
    for i in range(n):
        print(f" Punkt {i+1}")
        val_x = get_float_input(f" -> X: {val_x}")
        val_y = get_float_input(f" -> Y: {val_y}")
        
        x_pts.append(val_x)
        y_pts.append(val_y)

    x = np.array(x_pts)
    y = np.array(y_pts)
    
    if not np.all(np.diff(x) > 0):
        print("\n Błąd: Współrzędne X muszą być podane w porządku rosnącym!")
        print(" Upewnij się, że X1 < X2 < ... < Xn.")
        return

    cs = CubicSpline(x, y)
    
    x_fine = np.linspace(x.min(), x.max(), 300)
    y_interp = cs(x_fine)
    
    print("\n Obliczenia zakończone sukcesem. Generowanie wykresu...")
    
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color='red', s=60, zorder=5, label='Punkty węzłowe (Dane)')
    plt.plot(x_fine, y_interp, color='blue', linewidth=2, label='Interpolacja (Cubic Spline)')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='-')
    plt.axvline(0, color='black', linewidth=0.8, linestyle='-')
    x_margin = (x.max() - x.min()) * 0.05 if x.max() != x.min() else 1
    y_min = min(y.min(), y_interp.min())
    y_max = max(y.max(), y_interp.max())
    y_margin = (y_max - y_min) * 0.05 if y_max != y_min else 1
    plt.xlim(x.min() - x_margin, x.max() + x_margin)
    plt.ylim(y_min - y_margin, y_max + y_margin)
    plt.title('Interpolacja Splajnem Sześciennym')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.show()

"""========================================================================================================================================================"""

def solve_approximation():
    print("\n\t--- 5. Aproksymacja (Metoda Najmniejszych Kwadratów) ---")
    print(" Proces: szukamy ogólnego trendu dla podanych punktów za pomocą wielomianu stopnia 'd'.")
    print(" Wykres NIE MUSI przechodzić przez punkty, ale pokaże ogólną zależność (zredukuje szum).")
    
    n = int(get_float_input(" Wprowadź liczbę punktów: "))
    if n < 2:
        print("\n Błąd: Potrzebujesz co najmniej 2 punktów.")
        return
        
    deg = int(get_float_input(" Wprowadź stopień wielomianu (np. 1 dla prostej, 2 dla paraboli): "))
    if deg >= n:
        print(f"\n Błąd: Stopień wielomianu ({deg}) musi być mniejszy niż liczba punktów ({n})!")
        return

    x_pts = []
    y_pts = []
    
    for i in range(n):
        print(f"\n Punkt {i+1}")
        val_x = get_float_input(f" -> X: ")
        val_y = get_float_input(f" -> Y: ")
        x_pts.append(val_x)
        y_pts.append(val_y)

    x = np.array(x_pts)
    y = np.array(y_pts)
    
    coefficients = np.polyfit(x, y, deg)
    poly_function = np.poly1d(coefficients)
    
    print("\n Otrzymany wielomian aproksymacyjny (od najwyższej potęgi):")
    print(poly_function)
    
    x_fine = np.linspace(x.min(), x.max(), 300)
    y_approx = poly_function(x_fine)
    
    print("\n Obliczenia zakończone sukcesem. Generowanie wykresu...")
    
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color='red', s=60, zorder=5, label=' Punkty pomiarowe ')
    plt.plot(x_fine, y_approx, color='green', linestyle='--', linewidth=2.5, label=f'Aproksymacja (Stopień {deg})')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='-')
    plt.axvline(0, color='black', linewidth=0.8, linestyle='-')
    x_margin = (x.max() - x.min()) * 0.05 if x.max() != x.min() else 1
    y_min = min(y.min(), y_approx.min())
    y_max = max(y.max(), y_approx.max())
    y_margin = (y_max - y_min) * 0.05 if y_max != y_min else 1
    plt.xlim(x.min() - x_margin, x.max() + x_margin)
    plt.ylim(y_min - y_margin, y_max + y_margin)
    plt.title('Aproksymacja Wielomianowa (Metoda Najmniejszych Kwadratów)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.show()

"""========================================================================================================================================================"""

def main_menu():
    """Główne menu programu."""
    while True:
        print(f"    ============================================")
        print("              KALKULATOR MATEMATYCZNY")
        print( "    ============================================")
        print("\t1. Rozwiąż  równanie  nieliniowe  (Bisekcja)")
        print("\t2. Całkowanie  numeryczne  (Trapezy)")
        print("\t3. Układy  równań  liniowych  (Metoda  Gaussa)")
        print("\t4. Interpolacja  (Cubic  Spline)")
        print("\t5. Aproksymacja  (Wielomianowa Metoda Najmniejszych Kwadratów)")
        print("\t0. Wyjście")

        choice = input("    Wybierz działanie: ")
        if choice == '1':
            solve_nonlinear()
        elif choice == '2':
            solve_integration() 
        elif choice == '3':
            solve_linear_systems()
        elif choice == '4':
            solve_interpolation()
        elif choice == '5':
            solve_approximation()
        elif choice == '0':
            print("     Dziękujemy za użycie!")
            break
        else:
            print("\n Niewłaściwy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main_menu()

"""========================================================================================================================================================"""