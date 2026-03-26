import streamlit as st
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import random

# --- Ställ in sidans layout till bred ---
st.set_page_config(layout="wide", page_title="Läs av grafen")

# --- Specialdesign (CSS) för att göra text och rutor större ---
st.markdown("""
<style>
/* Gör texten som eleven skriver i svarsrutan mycket större och centrerad */
input[type="text"] {
    font-size: 24px !important;
    font-weight: bold !important;
    text-align: center !important;
    padding: 15px !important;
}
/* Gör etiketten (t.ex. 'Svar 1:') ovanför rutan större */
.stTextInput label p {
    font-size: 18px !important;
    font-weight: bold !important;
}
/* Gör rätt/fel-meddelandena lite tydligare */
.stAlert p {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# --- Funktioner ---
def generera_funktion():
    typ = random.choice(['linjar', 'kvadratisk'])
    
    if typ == 'linjar':
        k = random.choice([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2])
        m = random.randint(-4, 4)
        return lambda x: k * x + m
    else:
        a = random.choice([-1, -0.5, 0.5, 1])
        h = random.randint(-3, 3)
        v = random.randint(-4, 4)
        return lambda x: a * (x - h)**2 + v

def ny_uppgift():
    if 'fraga_nr' not in st.session_state:
        st.session_state.fraga_nr = 1
    else:
        st.session_state.fraga_nr += 1
        
    niva = st.session_state.get('niva', 1)
        
    for _ in range(100): 
        f = generera_funktion()
        
        giltiga_punkter = []
        for x_val in [i / 2 for i in range(-16, 17)]:
            y_val = f(x_val)
            if abs(y_val) <= 10 and round(y_val * 2, 4).is_integer():
                giltiga_punkter.append((round(x_val, 4), round(y_val, 4)))
                
        if not giltiga_punkter:
            continue 

        if niva == 1:
            target_x, target_y = random.choice(giltiga_punkter)
            fraga_typ = random.choice(['hitta_y', 'hitta_x'])
            
            if fraga_typ == 'hitta_y':
                fraga = f"Bestäm f({target_x:g})"
                ratt_svar = [target_y]
            else:
                target_y_snygg = target_y + 0.0 
                fraga = f"Bestäm ett värde på x så att f(x) = {target_y_snygg:g}"
                alla_x = list(set([p[0] for p in giltiga_punkter if p[1] == target_y]))
                ratt_svar = sorted(alla_x)
                
            break 
            
        else:
            fraga_typ = random.choice(['f_x_plus_c', 'f_f_c', 'f_a_op_f_b', 'f_kx'])
            
            if fraga_typ == 'f_x_plus_c':
                hel_punkter = [p for p in giltiga_punkter if round(p[1], 4).is_integer()]
                if not hel_punkter: continue
                
                target_x, target_y = random.choice(hel_punkter)
                c = random.choice([-3, -2, -1, 1, 2, 3])
                c_str = f"+ {c}" if c > 0 else f"- {abs(c)}"
                
                target_y_snygg = target_y + 0.0
                fraga = f"Bestäm x om f(x {c_str}) = {target_y_snygg:g}"
                
                alla_mål_x = [p[0] for p in giltiga_punkter if p[1] == target_y]
                ratt_svar = sorted([tx - c for tx in alla_mål_x])
                break
                
            elif fraga_typ == 'f_f_c':
                valid_c = []
                for x_val in range(-8, 9):
                    y1 = f(x_val)
                    if round(y1, 4).is_integer() and -8 <= y1 <= 8:
                        y2 = f(y1)
                        if abs(y2) <= 10 and round(y2 * 2, 4).is_integer():
                            valid_c.append(x_val)
                            
                if not valid_c: continue 
                
                c = random.choice(valid_c)
                ratt_svar = [f(f(c))]
                fraga = f"Bestäm f(f({c}))"
                break
                
            elif fraga_typ == 'f_a_op_f_b':
                hel_punkter = [p for p in giltiga_punkter if round(p[1], 4).is_integer() and round(p[0], 4).is_integer()]
                if len(hel_punkter) < 2: continue
                
                p1, p2 = random.sample(hel_punkter, 2)
                op = random.choice(['+', '-'])
                
                if op == '+':
                    svar = p1[1] + p2[1]
                else:
                    svar = p1[1] - p2[1]
                    
                fraga = f"Bestäm f({p1[0]:g}) {op} f({p2[0]:g})"
                ratt_svar = [svar]
                break
                
            elif fraga_typ == 'f_kx':
                mål_y = random.choice([p[1] for p in giltiga_punkter])
                alla_mål_x = [p[0] for p in giltiga_punkter if p[1] == mål_y]
                
                k_val = random.choice([2, -2, 0.5, -0.5, -1])
                
                mojliga_svar = [x / k_val for x in alla_mål_x]
                
                if all(round(s * 2, 4).is_integer() and abs(s) <= 20 for s in mojliga_svar):
                    k_str = f"{k_val:g}"
                    mål_y_snygg = mål_y + 0.0
                    fraga = f"Bestäm x om f({k_str}x) = {mål_y_snygg:g}"
                    ratt_svar = sorted(mojliga_svar)
                    break
                else:
                    continue

    else:
        f = lambda x: x
        fraga = "Bestäm f(1)"
        ratt_svar = [1.0]

    st.session_state.f = f
    st.session_state.fraga = fraga.replace('.', ',')
    st.session_state.ratt_svar = [round(ans, 4) + 0.0 for ans in ratt_svar]

# --- Initiera appens minne ---
if 'niva' not in st.session_state:
    st.session_state.niva = 1
if 'fraga_nr' not in st.session_state:
    ny_uppgift()

# --- UI (Själva webbsidan) ---
st.title("Läs av grafen!")

col_graf, col_kontroller = st.columns([1.5, 1], gap="large")

with col_graf:
    fig, ax = plt.subplots(figsize=(6, 6))
    x_plot = np.linspace(-10, 10, 400)
    y_plot = st.session_state.f(x_plot)

    ax.plot(x_plot, y_plot, linewidth=2.5, color='blue')

    ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='gray')
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.set_xticks(np.arange(-10, 11, 1))
    ax.set_yticks(np.arange(-10, 11, 1))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')

    ax.text(10.2, 0, 'x', va='center', ha='left', fontsize=12, fontweight='bold')
    ax.text(0, 10.2, 'y', va='bottom', ha='center', fontsize=12, fontweight='bold')

    st.pyplot(fig)
    plt.close(fig) 

with col_kontroller:
    # --- Inställningar ---
    st.subheader("Inställningar")
    aktuellt_index = 0 if st.session_state.niva == 1 else 1
    ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index)
    
    if ny_niva != st.session_state.niva:
        st.session_state.niva = ny_niva
        ny_uppgift()
        st.rerun()
        
    st.divider() 
    
    # --- Uppgift och Svarsrutor ---
    st.subheader("Uppgift")
    
    # FIX: Gör frågetexten mycket större med hjälp av HTML
    st.markdown(f"<div style='font-size: 32px; font-weight: bold; color: #0056b3; margin-bottom: 20px;'>{st.session_state.fraga}</div>", unsafe_allow_html=True)
    
    antal_svar = len(st.session_state.ratt_svar)
    svar_lista = []
    
    for i in range(antal_svar):
        etikett = f"Svar {i+1}:" if antal_svar > 1 else "Skriv ditt svar här:"
        nyckel = f"input_{st.session_state.fraga_nr}_{i}"
        svar = st.text_input(etikett, key=nyckel)
        svar_lista.append(svar)
        
    st.write("") 
    
    knapp_col1, knapp_col2 = st.columns(2)
    
    with knapp_col1:
        rattat = st.button("Rätta svar", type="primary", use_container_width=True)
        
    with knapp_col2:
        ny_graf = st.button("Ny graf", use_container_width=True)
        
    if ny_graf:
        ny_uppgift()
        st.rerun()
        
    if rattat:
        if all(s.strip() != "" for s in svar_lista):
            try:
                anv_svar_float = [round(float(s.strip().replace(',', '.')), 4) for s in svar_lista]
                
                if sorted(anv_svar_float) == st.session_state.ratt_svar:
                    st.success("✅ Helt rätt! Snyggt jobbat.")
                else:
                    svar_str = ' och '.join([f"{a:g}".replace('.', ',') for a in st.session_state.ratt_svar])
                    st.error(f"❌ Tyvärr fel. Rätt svar var: {svar_str}")
            except ValueError:
                st.warning("⚠️ Ange bara siffror (t.ex. 2, -3, eller 1,5).")
        else:
            st.warning("Fyll i alla rutor innan du rättar.")
