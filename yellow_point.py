import tkinter as tk


def print_matrix(dots):
    # Print the matrix of dots on standard output.
    print("           111111")
    print("  123456789012345")
    for y in range(7, -1, -1):
        line = ""
        for x in range(1, 16):
            if dots[(x,y)]:
                line += "o"
            else:
                line += " "
        print(y, line)

dots = {}
for row in range(8):
    for col in range(1,16):
        dots[(col, row)] = 0


def column_value(col, dots):
    # Extract and decode the value of the indicated column.
    total = 0
    for y in range(6, -1, -1):
        total += dots[(col, y)] * 2**y
    return total

def show(dots):
    text = ""
    if not 1 in dots.values():
        text+="This pattern is empty and cannot be interpreted."
        return text

    text+="Ignoring parity errors for odd rows and columns."

    # Decode serial number
    serial_number = tuple(map(lambda col: column_value(col, dots), (13, 12, 11))) + tuple(map(lambda col: column_value(col, dots), (14, 13, 12, 11)))
    text += "\n\nPrinter serial number: %02i%02i%02i [or %02i%02i%02i%02i]" % serial_number

    # Decode date and time
    year = column_value(8, dots)
    if year < 70 or year > 99:
        year += 2000
    else:
        year += 1900

    month_names = ["(no month specified)", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    try:
        month = month_names[column_value(7, dots)]
    except IndexError:
        month = "(invalid month %i)" % column_value(8, dots)

    day = column_value(6, dots)
    if day == 0:
        day = "(no day specified)"
    elif day > 31:
        day = "(invalid day %i)" % day

    text += "\n\nEvent date and time:"
    text += f"\nhh   : {column_value(5, dots)}"
    text += f"\nmm    : {column_value(2, dots)}"
    text += f"\ndd   : {day}"
    text += f"\nMM   : {month}"
    text += f"\nyyyy : {year}"
    text += f"\nSSSSSSSS : Serial number {column_value(15, dots)}"
    return text


def submit():
    # Fonction à appeler lorsque le bouton "Submit" est pressé
    # Réinitialiser la liste et effacer les sélections
    # Afficher le texte saisi dans l'espace à droite*
    print_matrix(dots)
    result_text = show(dots)
    text_area.delete(1.0, tk.END)  # Efface le texte précédent dans le widget de texte
    text_area.insert(tk.END, result_text)  # Insère le nouveau texte généré


def create_button(parent, row, col):
    def toggle_state(row, col):
        # Fonction pour changer l'état du bouton (jaune ou blanc)
        if circle_button["bg"] == "yellow":
            circle_button["bg"] = "white"
            dots[(col+1, 7-row)] = 0
        else:
            circle_button["bg"] = "yellow"
            dots[(col+1, 7-row)] = 1
        print(dots)


    # Créer un bouton rond jaune à la position (row, col)
    circle_button = tk.Button(parent, text="", bg="white", command=lambda:toggle_state(row, col))
    circle_button.grid(row=row, column=col)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Points jaune imprimante")

# Créer les boutons ronds jaunes
for row in range(8):
    for col in range(15):
        create_button(root, row, col)

# Créer l'espace de texte à droite
text_area = tk.Text(root, height=17, width=30)
text_area.grid(row=0, column=16, rowspan=9)  # Augmenter rowspan à 8 pour occuper toute la hauteur de la fenêtre


# Créer le bouton "Submit"
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=8, column=0, columnspan=15)

root.mainloop()
