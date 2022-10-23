from tkinter import *
import sympy
import re


window = Tk()
window.title("Balancing Chemical Equations Calculator")
window.geometry("1440x1024")
window.configure(bg = "#e6f3ff")
canvas = Canvas(
    window,
    bg = "#e6f3ff",
    height = 1024,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    716.5, 512.0,
    image=background_img)



############################################### RESULT ######################################################

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    1020.0, 780,
    image = entry0_img)

entry0 = Label(
    window,
    text="",
    bg="#ffffff",
    fg="#585E8F",
    font=("Century Gothic", 18))

entry0.place(
    x = 740.0, y = 739,
    width = 560.0,
    height = 63)

############################################### PRODUCT ###############################################
def returnEntry1(arg=None):
    """Gets the result from Entry and return it to the Label"""

    result1 = entry1.get()
    entry0.config(text=result1)
    entry1.delete(0, END)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    1020.0, 528,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    fg="#585E8F",
    font=("Century Gothic", 18),
    highlightthickness = 0)
entry1.bind("<Return>", returnEntry1)
entry1.pack()

entry1.place(
    x = 740.0, y = 488,
    width = 560.0,
    height = 63)

############################################### REACTANT ###############################################
def returnEntry2(arg=None):
    """Gets the result from Entry and return it to the Label"""

    result2 = entry2.get()
    entry0.config(text=result2)
    entry2.delete(0, END)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    1018.0, 390,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#ffffff",
    fg="#585E8F",
    font=("Century Gothic", 18),
    highlightthickness = 0)
entry2.bind("<Return>", returnEntry2)
entry2.pack()

entry2.place(
    x = 738.0, y = 351,
    width = 560.0,
    height = 63)




############################################# FORMULA ###################################################


# Find minimum integer coefficients for a chemical reaction like
#   A * NaOH + B * H2SO4 -> C * Na2SO4 + D * H20


# match a single element and optional count, like Na2
ELEMENT_CLAUSE = re.compile("([A-Z][a-z]?)([0-9]*)")

def parse_compound(compound):
    """
    Given a chemical compound like Na2SO4,
    return a dict of element counts like {"Na":2, "S":1, "O":4}
    """
    assert "(" not in compound, "This parser doesn't grok subclauses"
    return {el: (int(num) if num else 1) for el, num in ELEMENT_CLAUSE.findall(compound)}

def main():
    lhs_strings = entry2.get().split("+")
    lhs_compounds = [parse_compound(compound) for compound in lhs_strings]

    rhs_strings = entry1.get().split("+")
    rhs_compounds = [parse_compound(compound) for compound in rhs_strings]

    # Get canonical list of elements
    els = sorted(set().union(*lhs_compounds, *rhs_compounds))
    els_index = dict(zip(els, range(len(els))))

    # Build matrix to solve
    w = len(lhs_compounds) + len(rhs_compounds)
    h = len(els)
    A = [[0] * w for _ in range(h)]
    # load with element coefficients
    for col, compound in enumerate(lhs_compounds):
        for el, num in compound.items():
            row = els_index[el]
            A[row][col] = num
    for col, compound in enumerate(rhs_compounds, len(lhs_compounds)):
        for el, num in compound.items():
            row = els_index[el]
            A[row][col] = -num   # invert coefficients for RHS

    # Solve using Sympy for absolute-precision math
    A = sympy.Matrix(A)
    # find first basis vector == primary solution
    coeffs = A.nullspace()[0]
    # find least common denominator, multiply through to convert to integer solution
    coeffs *= sympy.lcm([term.q for term in coeffs])


    # Display result
    lhs = " + ".join(["{} {}".format(coeffs[i], s) for i, s in enumerate(lhs_strings)])
    rhs = " + ".join(["{} {}".format(coeffs[i], s) for i, s in enumerate(rhs_strings, len(lhs_strings))])
    answer = ("{} → {}".format(lhs, rhs))
    print(answer)
    entry0.config(text=answer)

############################################### RESULT ###############################################


img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command= main,
    relief = "flat")

b0.place(
    x = 888, y = 597,
    width = 265,
    height = 75)

window.resizable(False, False)
window.mainloop()