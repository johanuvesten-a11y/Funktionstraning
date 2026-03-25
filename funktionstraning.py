import matplotlib.pyplot as plt
import numpy as np
import random

def generera_funktion():
    """Slumpar fram en rät linje eller en andragradsfunktion med 'snälla' värden."""
    typ = random.choice(['linjar', 'kvadratisk'])
    
    if typ == 'linjar':
        # Räta linjens ekvation: y = kx + m
        k = random.choice([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2])
        m = random.randint(-4, 4)
        def f(x): return k * x + m
        
    else:
        # Andragradsekvation: y = a(x-h)^2 + v
        a = random.choice([-1, -0.5, 0.5, 1])
        h = random.randint(-3, 3)
        v = random.randint(-4, 4)
        def f(x): return a * (x - h)**2 + v
        
    return f

def run_quiz():
    print("==================================================")
    print(" Välkommen till funktionsträningen! ")
    print(" Läs av grafen som dyker upp och svara i fönstret.")
    print(" Skriv 'q' för att avsluta programmet.")
    print("==================================================\n")
    
    # Skapar ett fönster för grafen
    plt.ion() 
    fig, ax = plt.subplots(figsize=(7, 7))
    
    while True:
        f = generera_funktion()
        
        # Hitta giltiga punkter där både x och y är hel- eller halvtal
        giltiga_punkter = []
        for x_val in np.arange(-8, 8.5, 0.5):
            y_val = f(x_val)
            # Kolla om y är ett hel- eller halvtal och ryms i fönstret (-10 till 10)
            if abs(y_val) <= 10 and (y_val * 2).is_integer():
                giltiga_punkter.append((x_val, y_val))
                
        if not giltiga_punkter:
            continue # Om vi mot förmodan inte hittar bra punkter, slumpa ny

        # Välj en slumpmässig punkt som ska vara svaret
        target_x, target_y = random.choice(giltiga_punkter)
        
        # Slumpa frågetyp: f(a) = ? eller f(x) = b
        fraga_typ = random.choice(['hitta_y', 'hitta_x'])
        
        if fraga_typ == 'hitta_y':
            fraga = f"Vad är f({target_x:g})?"
            ratt_svar = [target_y]
        else:
            fraga = f"Bestäm ett x-värde så att f(x) = {target_y:g}."
            # För andragradare kan det finnas två x-värden som ger samma y
            ratt_svar = [p[0] for p in giltiga_punkter if p[1] == target_y]

        # Rita grafen
        ax.clear()
        x_plot = np.linspace(-10, 10, 400)
        y_plot = f(x_plot)
        
        ax.plot(x_plot, y_plot, linewidth=2, color='blue')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.axhline(0, color='black', linewidth=1.5) # x-axeln
        ax.axvline(0, color='black', linewidth=1.5) # y-axeln
        
        # Ställ in rutnätet så varje heltal syns
        ax.set_xticks(np.arange(-10, 11, 1))
        ax.set_yticks(np.arange(-10, 11, 1))
        ax.set_xlim(-8, 8)
        ax.set_ylim(-10, 10)
        ax.set_title("Läs av grafen!", fontsize=14)
        ax.set_xlabel("x", fontsize=12)
        ax.set_ylabel("y", fontsize=12)
        
        plt.show()
        plt.pause(0.1) # Uppdatera grafen
        
        # Ta emot svar från användaren
        anvandar_svar = input(f"{fraga}\nSvar: ").strip().replace(',', '.')
        
        if anvandar_svar.lower() == 'q':
            print("Avslutar programmet. Bra jobbat idag!")
            break
            
        try:
            svar_float = float(anvandar_svar)
            if svar_float in ratt_svar:
                print("✅ Helt rätt! Snyggt jobbat.\n")
            else:
                svar_str = ' eller '.join([f"{a:g}" for a in ratt_svar])
                print(f"❌ Tyvärr fel. Rätt svar var: {svar_str}\n")
        except ValueError:
            print("⚠️ Felaktigt inmatningsformat. Ange bara siffror (t.ex. 2, -3, eller 1.5).\n")
            
        input("Tryck på [Enter] för att få en ny uppgift...")

if __name__ == "__main__":
    run_quiz()
