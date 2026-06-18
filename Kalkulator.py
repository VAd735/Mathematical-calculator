import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def get_float_input(prompt):
    "\n Funkcja pomocnicza umozliwiajaca bezpieczne wprowadzanie numerów."
    while True:
        try:
            return float(input(prompt))
        except ValueError: print("\n Blad wartosci! Prosze wprowadzic wartosc liczbowa.")

Bold = '\033[1m'
End = '\033[0m'

"""========================================================================================================================================================"""

def solve_nonlinear():
    print("\n\t--- 1. Rownania nieliniowe (Metoda bisekcji) ---")
    print(f" Rownanie za domyslnym: {Bold}f(x) = 3 × x² - 4{End}")
    
    print(f"\n {Bold}OPIS METODY BISEKCJI:{End}")
    print(" • To jest numer yczny metod do znalezienia pierwiastka funkcji f(x) = 0")
    print(" • Zasnowany na zasadzie 'dzielmy interval na pol' (bisekcja = roztin)")
    print(" • Wymaga, zeby funkcja byla nieprzerywna i zmienial znak na koncach intervalu")
    print(" • Prosty, niezawodny i gwarantowany proces zbieznosci")
    print(" • Nie wymaga liczenia pochodnych\n")
    
    print(f" {Bold}ALGORYTM:{End}")
    print(" 1. Zadajemy interval [a, b], gdzie f(a) i f(b) maja rozne znaki")
    print(" 2. Znajdujemy srodek: c = (a + b) / 2")
    print(" 3. Sprawdzamy znak f(c):")
    print("    - Jesli f(c) ma ten sam znak co f(a), to pierwiastek jest w [c, b]")
    print("    - Jesli f(c) ma ten sam znak co f(b), to pierwiastek jest w [a, c]")
    print(" 4. Powtarzamy az interval nie bedzie dostatecznie maly\n")
    
    f = lambda x: 3 * x**2 - 4
    
    a = get_float_input(" Wprowadz poczatek przedzialu (a): ")
    b = get_float_input(" Wprowadz koniec przedzialu (b): ")
    e = get_float_input(" Wprowadz dokladnosc (np. 0.0001): ")
    
    if f(a) * f(b) >= 0:
        print("\n Blad: Funkcja powinna miec rozne znaki na koncach przedzialu!")
        print(f" f({a:.2f}) = {f(a):.2f}")
        print(f" f({b:.2f}) = {f(b):.2f}")
        print(f" Iloczyn: f(a) * f(b) = {f(a) * f(b):.2f} > 0")
        print(" To oznacza, ze w podanym przedziale moze nie byc pierwiastka!")
        return
    
    print(f"\n {Bold}DETALE ROZWIAZANIA:{End}")
    print(f" Szukamy pierwiastka f(x) = 0 w przedziale [{a:.2f}, {b:.2f}]")
    print(f" Dokladnosc (maksymalna dopuszczalna blad): epsilon = {e}")
    print(f" Warunki poczatkowe: f({a:.2f}) = {f(a):.2f}, f({b:.2f}) = {f(b):.2f}")
    print(f" f({a:.2f}) * f({b:.2f}) = {f(a)*f(b):.2f} < 0 ✓ (znaki rozne)\n")
    
    krok = 0
    while (b - a) / 2 > e:
        krok += 1
        xc = (a + b) / 2
        fm = f(xc)
        print(f" ┌─ KROK {krok}: ─────────────────────────────────────────")
        print(f" │ Aktualny interval: [{a:.2f}, {b:.2f}], szerokosc = {(b-a):.2f}")
        print(f" │ Srodek c = {xc:.2f}")
        print(f" │ Wartosci: f({a:.2f})={f(a):7.4f}, f({xc:.2f})={fm:7.4f}, f({b:.2f})={f(b):7.4f}")
        
        if abs(fm) < 1e-10:
            print(" │ SUKCES! Znaleziono dokładny pierwiastek!")
            print(" └─────────────────────────────────────────────────────")
            b = xc
            break
        elif f(a) * fm < 0:
            print(f" │ Wniosek: f({a:.2f}) i f({xc:.2f}) maja rozne znaki")
            print(f" │ Pierwiastek jest LEWY od {xc:.2f}")
            print(f" │ Nowy interval: [{a:.2f}, {xc:.2f}]")
            print(" └─────────────────────────────────────────────────────")
            b = xc
        else:
            print(f" │ Wniosek: f({xc:.2f}) i f({b:.2f}) maja rozne znaki")
            print(f" │ Pierwiastek jest PRAWY od {xc:.2f}")
            print(f" │ Nowy interval: [{xc:.2f}, {b:.2f}]")
            print(" └─────────────────────────────────────────────────────")
            a = xc
    
    x_result = (a + b) / 2
    print(f"\n {Bold}FINALNY REZULTAT:{End}")
    print(f" Liczba krokow wykonanych: {krok}")
    print(f" Finalny interval: [{a:.2f}, {b:.2f}]")
    print(f" Szerokosc: {(b-a):.2f} <= {e} (dokladnosc osiagnieta)")
    print(f" Pierwiastek (przybliżenie): x ≈ {x_result:.2f}")
    print(f" Sprawdzenie: f({x_result:.2f}) = {f(x_result):.2f}")
    print(f"\n ★★★ ROZWIAZANIE ZNALEZIONE: x ≈ {x_result:.2f} ★★★\n")

"""========================================================================================================================================================"""

def solve_integration():
    print("\n\t--- 2. Calkowanie numeryczne (Metoda trapezow) ---")
    print(" Wprowadz funkcje w formacie Python (np. 3 * x**2 - 4 lub x**3 + 2*x):")
    funkcja = input(" f(x) = ")
    
    try:
        f = lambda x: eval(funkcja)
        # Test
        f(0)
    except:
        print(" Blad! Nieprawidlowa funkcja!")
        return
    
    print(f"\n Calkowanie funkcji: {Bold}f(x) = {funkcja}{End}")
    
    print(f"\n {Bold}OPIS METODY TRAPEZOW:{End}")
    print(" • To jest numer iczny metod do przyblizonego obliczenia calki oznaczonej")
    print(" • Zamiast dokładnego obliczania, aproksymujemy pole pod krzywa suma trapezow")
    print(" • Kazda trapezja to geometryczna figura z rownoleglymai podstawami")
    print(" • Im wiecej trapezow (wieksze n), tym dokładniejsze przybliżenie")
    print(f" • Podstawowy wzor: pole trapezji = {Bold}h × (f(a) + f(b))/2{End}\n")
    
    print(f" {Bold}ALGORYTM:{End}")
    print(" 1. Dzielimy interval [a, b] na n rownych czesci szerokosci h = (b - a) / n")
    print(" 2. Na kazdej czesci aproksymujemy funkcje trapezja")
    print(" 3. Pole kazdej trapezji = h × (f(xi) + f(xi+1))/2")
    print(" 4. Sumujemy pola wszystkich trapezow")
    print(f" 5. Wynik: {Bold}Całka ≈ h × [f(x0)/2 + f(x1) + f(x2) + ... + f(xn)/2]{End}\n")
    
    a = get_float_input(" Wprowadz nizszą granic (a): ")
    b = get_float_input(" Wprowadz gorną granice (b): ")
    n = int(get_float_input(" Wprowadz liczbe podzialow (n): "))
    
    if n < 1:
        print(" Blad! Liczba podzialow musi byc >= 1")
        return

    h = (b - a) / n
    
    print(f"\n {Bold}DETALE ROZWIAZANIA:{End}")
    print(f" Interval calkowania: [{a:.2f}, {b:.2f}]")
    print(f" Liczba trapezow (podzialow): n = {n}")
    print(f" Szerokosc kazdego przedzialu: h = ({b:.2f} - {a:.2f}) / {n} = {h:.2f}")
    print(f" Punkty podziału: x0={a:.2f}, x1, x2, ..., x{n}={b:.2f}\n")
    
    print(" Tabela wartosci funkcji w punktach podziału:")
    print(" ┌──────┬──────────────┬──────────────┐")
    print(" │  i   │      xi      │     f(xi)    │")
    print(" ├──────┼──────────────┼──────────────┤")
    
    x = a
    suma = 0
    
    for i in range(n + 1):
        wartosc = f(x)
        if i == 0 or i == n:
            print(f" │{i:^4}  │{x:12.4f}  │{wartosc:12.6f}  │  (koniec)")
        else:
            print(f" │{i:^4}  │{x:12.4f}  │{wartosc:12.6f}  │")
            suma += wartosc
        x += h
    
    print(f" └──────┴──────────────┴──────────────┘\n")
    
    wynik = h * ((f(a) + f(b)) / 2 + suma)
    
    print(f" {Bold}WZOR I OBLICZENIA:{End}")
    print(f" Całka ≈ h × [f(x0)/2 + f(x1) + ... + f(x{n})/2]")
    print(f" Całka ≈ h × [f({a:.2f})/2 + (suma wnętrza) + f({b:.2f})/2]")
    print(f" Suma wartosci we wnętrzu: {suma:.4f}")
    print(f" Suma z połowami koncow: {((f(a) + f(b)) / 2 + suma):.4f}")
    print(f" Wynik: {h:.4f} × {((f(a) + f(b)) / 2 + suma):.4f} = {wynik:.4f}")
    print(f"\n ★★★ WYNIK CALKOWANIA: ∫f(x)dx ≈ {wynik:.4f} ★★★\n")

"""========================================================================================================================================================"""

def solve_linear_systems():
    print("\n\t--- 3. Systemy rownan liniowych (metoda Gaussa) ---")
    
    print(f"\n {Bold}OPIS METODY GAUSSA:{End}")
    print(" • Klasyczny metod do rozwiazania systemow rownan liniowych")
    print(" • Transformuje macierz do postaci trójkątnej (eliminacja Gaussa)")
    print(" • Nastepnie uzywa podstawiania wstecznego do znalezienia zmiennych")
    print(" • Wybiera element maksymalny (pivot) dla stabilnosci numerycznej")
    print(" • Zlozonosc: O(n³)\n")
    print(f"\n {Bold}ALGORYTM:{End}")
    print(" 1. Tworzymy rozszerzoną macierz [A|b], gdzie A - wspoldzynniki, b - wolne wyrazy")
    print(" 2. PRZÓD (eliminacja Gaussa):")
    print("    - Dla kazdego wiersza wybieramy maksymalny element (pivot)")
    print("    - Normalizujemy wiersz na ten element")
    print("    - Eliminujemy zmienną z nizszych wierszy")
    print(" 3. WSTECZ (podstawianie wsteczne): liczymy zmienne od dolu do gory\n")
    print("\n Wybierz rozmiar macierzy:")
    print(" 1. [2 × 3]")
    print(" 2. [3 × 3]")
    print(" 3. [4 × 3]")
    print(" 4. [4 × 4]")
    print(" 5. [5 × 3]")
    print(" 6. [5 × 4]")
    print(" 7. [5 × 5]")

    choice = input(" Wybierz rozmiar (1-7): ")
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
        print("\n Niew lasciwy wybor.")
        return
    
    print(f"\n Wybrano rozmiar [{n}×{m}]")
    print(f" {Bold}DETALE ROZWIAZANIA:{End} ")
    
    matrix = []
    for i in range(n):
        print(f"\n Rownanie {i+1}:")
        row = []
        for j in range(m):
            coeff = get_float_input(f"  Wspoldzynnik x{j+1}: ")
            row.append(coeff)
        const = get_float_input("  Wyraz wolny (po =): ")
        row.append(const)
        matrix.append(row)

    print("\n POCZATKOWA MACIERZ:")
    for i, row in enumerate(matrix):
        s = " | ".join([f"{row[j]:8.2f}" for j in range(m)]) + f" | {row[m]:8.2f}"
        print(f" Rownanie {i+1}: {s}")
    
    print(f"\n {Bold}PRZOD - ELIMINACJA GAUSSA:{End}")
    
    for i in range(min(n, m)):
        print(f"\n ┌─ KROK {i+1}: Obrobka kolumny {i+1} ─────────────────────")
        
        pivot_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[pivot_row][i]):
                pivot_row = k

        if pivot_row != i:
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            print(f" │ Zamiana: Wiersz {i+1} ↔ Wiersz {pivot_row+1}")
        
        pivot = matrix[i][i]
        print(f" │ Pivot element: {pivot:.2f}")
        
        if abs(pivot) < 1e-10:
            print(" │ ⚠ Pivot bliski zeru - pomijamy")
            print(" └──────────────────────────────────")
            continue

        for k in range(i, m + 1):
            matrix[i][k] /= pivot
        print(f" │ Normalizacja: Wiersz {i+1} podzielono przez pivot")
        
        for j in range(i + 1, n):
            factor = matrix[j][i]
            if abs(factor) > 1e-10:
                print(f" │ Eliminacja: Wiersz {j+1} = Wiersz {j+1} - ({factor:.2f}) × Wiersz {i+1}")
                for k in range(i, m + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        print(" └──────────────────────────────────")

    print("\n MACIERZ PO ELIMINACJI (postac trojkątna):")
    for i, row in enumerate(matrix):
        s = " | ".join([f"{row[j]:8.4f}" for j in range(m)]) + f" | {row[m]:8.4f}"
        print(f" Wiersz {i+1}: {s}")
    
    if n == m:
        print(f"\n {Bold}WSTECZ - PODSTAWIANIE WSTECZNE:{End}")
        x_res = [0 for _ in range(n)]
        
        for i in range(n - 1, -1, -1):
            print(f"\n ┌─ Obliczenie x{i+1}: ──────────────────────────")
            x_res[i] = matrix[i][n]
            print(f" │ Rownanie {i+1}: x{i+1}", end="")
            
            for k in range(i + 1, n):
                if abs(matrix[i][k]) > 1e-10:
                    print(f" + ({matrix[i][k]:.2f})×x{k+1}", end="")
                    x_res[i] -= matrix[i][k] * x_res[k]
            
            print(f" = {matrix[i][n]:.2f}")
            print(" │ Podstawiajac juz znane wartosci:")
            for k in range(i + 1, n):
                if abs(matrix[i][k]) > 1e-10:
                    print(f" │   Odejmujemy: {matrix[i][k]:.2f} × {x_res[k]:.2f} = {matrix[i][k]*x_res[k]:.2f}")
            
            print(f" │ Wynik: x{i+1} = {x_res[i]:.4f}")
            print(" └──────────────────────────────────")
        
        print(f"\n {Bold}FINALNY WYNIK:{End}")
        for i, x in enumerate(x_res):
            print(f" x{i+1} = {x:.4f}")
        print(f"\n ★★★ ROZWIAZANIE: {', '.join([f'x{i+1}={x:.4f}' for i, x in enumerate(x_res)])} ★★★\n")
    else:
        print("\n ⚠ System nie jest kwadratowy - nie ma jednoznacznego rozwiazania")
        print(" Macierz w postaci echelonnej jest pokazana wyzej.")

"""========================================================================================================================================================"""

def solve_interpolation():
    print("\n\t--- 4. Interpolacja (Cubic Spline) ---")
    
    print(f"\n {Bold}OPIS METODY CUBIC SPLINE:{End}")
    print(" • To metod gładkiej interpolacji, ktora przechodzi DOKLADNIE przez wszystkie podane punkty")
    print(" • Uzywa kubicznych (trzeciego stopnia) wielomianow do łączenia punktów")
    print(" • Na kazdy przedział między dwoma punktami przypada inny wielomian")
    print(" • Warunki gładkosci: funkcja i jej pochodne są ciągłe w punktach połączenia")
    print(" • Korzystnie dla tworzenia płynnych krzywych bez ostrych przeskoków")
    print(" • Czesto uzywane w grafice komputerowej i projektowaniu\n")
    print(f"\n {Bold}ALGORYTM PODSTAWOWY:{End}")
    print(" 1. Mamy n punktów (x0,y0), (x1,y1), ..., (xn,yn)")
    print(" 2. Znajdujemy n-1 wielomianów trzeciego stopnia dla każdego przedziału")
    print(" 3. Każdy wielomian S_i(x) = a + b(x-xi) + c(x-xi)² + d(x-xi)³ przechodzi przez punkty")
    print(" 4. Warunki: nieprzerywana funkcja, nieprzerywana pierwsza pochodna, nieprzerywana druga pochodna\n")
    
    n = int(get_float_input(" Wprowadz liczbe punktów (minimum 2): "))
    if n < 2:
        print("\n Blad: Do interpolacji splajnami potrzebne są co najmniej 2 punkty.")
        return
        
    x_pts = []
    y_pts = []
    
    print(f"\n {{Bold}}WEJSCIE DANYCH:{{End}}")
    print(" Podaj współrzędne punktów (można uzywac liczb ujemnych)")
    print(" WAZNE: Wspoldrzedne X musza byc w ROSNACYM porzadku!\n")
    
    for i in range(n):
        print(f" Punkt {i+1}:")
        val_x = get_float_input(f"  X: ")
        val_y = get_float_input(f"  Y: ")
        x_pts.append(val_x)
        y_pts.append(val_y)

    x = np.array(x_pts)
    y = np.array(y_pts)
    
    if not np.all(np.diff(x) > 0):
        print("\n Blad: Wspoldrzedne X musza byc w porządku rosnacym!")
        print(" Upewnij sie, ze X1 < X2 < ... < Xn.")
        return

    print(f"\n {Bold}WPROWADZONE PUNKTY:{End}")
    for i in range(n):
        print(f" Punkt {i+1}: ({x[i]:.2f}, {y[i]:.2f})")

    print(f"\n {Bold}OBLICZANIE KUBICZNYCH SPLAJNÓW:{End}")
    print(f" Dla {{Bold}}{n-1} przedziałów{{End}}...")
    
    cs = CubicSpline(x, y)
    
    x_fine = np.linspace(x.min(), x.max(), 300)
    y_interp = cs(x_fine)
    
    print(" ✓ Splajny pomyslnie obliczone")
    print(" ✓ Wszystkie wprowadzone punkty włączone do interpolacji")
    print(" ✓ Krzywa przechodzi DOKLADNIE przez każdy punkt\n")
    
    print(" Generowanie wykresu...")
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red', s=100, zorder=5, label='Punkty węzłowe (dane)', marker='o')
    plt.plot(x_fine, y_interp, color='blue', linewidth=2.5, label='Interpolacja (Cubic Spline)', zorder=3)
    plt.axhline(0, color='gray', linewidth=0.8, linestyle='-', alpha=0.3)
    plt.axvline(0, color='gray', linewidth=0.8, linestyle='-', alpha=0.3)
    plt.grid(True, linestyle=':', alpha=0.4)
    
    x_margin = (x.max() - x.min()) * 0.1 if x.max() != x.min() else 1
    y_min = min(y.min(), y_interp.min())
    y_max = max(y.max(), y_interp.max())
    y_margin = (y_max - y_min) * 0.1 if y_max != y_min else 1
    
    plt.xlim(x.min() - x_margin, x.max() + x_margin)
    plt.ylim(y_min - y_margin, y_max + y_margin)
    plt.title('Interpolacja Splajnem Sześciennym (Cubic Spline)', fontsize=14, fontweight='bold')
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()
    
    print(" ★★★ INTERPOLACJA ZAKONCZONA POWODZENIEM ★★★\n")

"""========================================================================================================================================================"""

def solve_approximation():
    print("\n\t--- 5. Aproksymacja (Metoda Najmniejszych Kwadratów) ---")
    
    print(f"\n {{Bold}}OPIS METODY NAJMNIEJSZYCH KWADRATÓW:{{End}}")
    print(" • Metod do znalezienia przyblizonej zaleznosci między zmiennymi")
    print(" • Na różnicę od interpolacji, krzywa NIE MUSI przechodzić przez punkty")
    print(" • Minimalizuje sumę kwadratów błędów: min Σ(f(xi) - yi)²")
    print(" • Korzystna dla danych z szumem lub gdy potrzebny jest ogólny trend")
    print(" • Mozna wybrać stopień wielomianu dla kontroli gładkosci")
    print(" • Prostsza obliczeniowo niz interpolacja\n")
    print(f"\n {{Bold}}ALGORYTM:{{End}}")
    print(" 1. Wybieramy stopień wielomianu d")
    print(" 2. Szukamy wielomianu p(x) = a0 + a1 × x + a2 × x² + ... + ad × x^d")
    print(" 3. Wspoldzynniki obliczane aby zminimalizowac sume kwadratów odchylen")
    print(" 4. Mozna liczyć bledy przybliżenia (MSE, RMSE)\n")
    
    n = int(get_float_input(" Wprowadz liczbe punktów: "))
    if n < 2:
        print("\n Blad: Potrzebujesz co najmniej 2 punktów.")
        return
    
    print(f"\n {{Bold}}WYBOR STOPNIA WIELOMIANU:{{End}}")
    print(" - Stopień 1: liniowa funkcja (prosta linia)")
    print(" - Stopień 2: kwadratowa funkcja (parabola)")
    print(" - Stopień 3: kubiczna funkcja (S-podobna krzywa)")
    print(" - Wyzsze stopnie: bardziej złozone formy")
    print(" UWAGA: Stopień musi byc < liczba punktów\n")
        
    deg = int(get_float_input(" Wprowadz stopień wielomianu (1, 2, 3, ...): "))
    if deg >= n:
        print(f"\n Blad: Stopień wielomianu ({deg}) musi byc mniejszy niz liczba punktów ({n})!")
        print(f" Rekomendacja: uzyj stopnia <= {n-1}")
        return

    x_pts = []
    y_pts = []
    
    print(f"\n {{Bold}}WEJSCIE DANYCH:{{End}}")
    for i in range(n):
        print(f" Punkt {i+1}:")
        val_x = get_float_input(f"  X: ")
        val_y = get_float_input(f"  Y: ")
        x_pts.append(val_x)
        y_pts.append(val_y)

    x = np.array(x_pts)
    y = np.array(y_pts)
    
    print(f"\n {{Bold}}OBLICZANIE APROKSYMUJACEGO WIELOMIANU:{{End}}")
    print(f" Liczba punktów: {n}")
    print(f" Stopień wielomianu: {deg}")
    print(" Obliczanie wspoldzynników...")
    
    coefficients = np.polyfit(x, y, deg)
    poly_function = np.poly1d(coefficients)
    
    print(f"\n {{Bold}}OTRZYMANY WIELOMIAN:{{End}}")
    print(poly_function)
    
    y_calc = poly_function(x)
    errors = y - y_calc
    mse = np.mean(errors**2)
    rmse = np.sqrt(mse)
    
    print(f"\n {{Bold}}JAKOŚĆ APROKSYMACJI:{{End}}")
    print(" Błędy w punktach:")
    for i in range(n):
        print(f"  Punkt {i+1}: y={y[i]:.2f}, y_calc={y_calc[i]:.2f}, błąd={errors[i]:+.6f}")
    
    print(f"\n Średnia kwadratowa błędu (MSE): {mse:.8f}")
    print(f" Pierwiastek MSE (RMSE): {rmse:.8f}")
    
    x_fine = np.linspace(x.min(), x.max(), 300)
    y_approx = poly_function(x_fine)
    
    print("\n Generowanie wykresu...")
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red', s=100, zorder=5, label='Punkty pomiarowe (dane)', marker='o')
    plt.plot(x_fine, y_approx, color='green', linestyle='-', linewidth=2.5, 
             label=f'Aproksymacja (stopień {deg})', zorder=3)
    for i in range(n):
        plt.plot([x[i], x[i]], [y[i], y_calc[i]], 'k--', alpha=0.3, linewidth=1)
    plt.axhline(0, color='gray', linewidth=0.8, linestyle='-', alpha=0.3)
    plt.axvline(0, color='gray', linewidth=0.8, linestyle='-', alpha=0.3)
    plt.grid(True, linestyle=':', alpha=0.4)
    
    x_margin = (x.max() - x.min()) * 0.1 if x.max() != x.min() else 1
    y_min = min(y.min(), y_approx.min())
    y_max = max(y.max(), y_approx.max())
    y_margin = (y_max - y_min) * 0.1 if y_max != y_min else 1
    
    plt.xlim(x.min() - x_margin, x.max() + x_margin)
    plt.ylim(y_min - y_margin, y_max + y_margin)
    plt.title(f'Aproksymacja Wielomianowa (Metoda Najmniejszych Kwadratów) - Stopień {deg}', 
              fontsize=14, fontweight='bold')
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()
    
    print(f" ★★★ APROKSYMACJA ZAKONCZONA - RMSE={rmse:.4f} ★★★\n")

"""========================================================================================================================================================"""

def main_menu():
    """Główne menu programu."""
    while True:
        print("═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ = = =")
        print("                  KALKULATOR MATEMATYCZNY              ")
        print("═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═")
        print("\t1. Równania nieliniowe (Bisekcja)")
        print("\t2. Całkowanie numeryczne (Trapezy)")
        print("\t3. Systemy równań liniowych (Gauss)")
        print("\t4. Interpolacja (Cubic Spline)")
        print("\t5. Aproksymacja (Najmniejsze Kwadraty)")
        print("\t0. Wyjście")

        choice = input("\n    Wybierz działanie: ")
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
            print("     Dziękujemy za skorzystanie z naszych usług, zapraszamy ponownie!")
            break
        else:
            print("\n Niewłaściwy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main_menu()
