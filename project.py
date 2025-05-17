import tkinter as tk  # Import tkinter for GUI
from tkinter import messagebox  # For displaying messagebox for validation and error messages
import tkinter.font as tkFont  # For customizing font styles

class ContactBook:
    def __init__(self, root):
        self.contacts = {}  # Dictionary to store contacts
        self.edit_mode = None  # Track the current edit mode
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("600x850")
        self.root.configure(bg="#B3EFFF")

        default_font = tkFont.Font(family="Roboto", size=11)
        root.option_add("*Font", default_font)

        # Title label
        tk.Label(root, text="Contact Book", font=("Roboto", 40, "bold"), bg="#B3EFFF").pack(pady=10)

        # Display area for output
        self.display = tk.Text(root, height=10, width=65, bg="#ffffff", state="disabled")
        self.display.pack(pady=10)

        # Dictionary of widgets (labels, entries, buttons)
        self.widgets = {
            "ref_label": tk.Label(root, text="Reference Number:", bg="#B3EFFF"),
            "ref_entry": tk.Entry(root, bg="white"),
            "name_label": tk.Label(root, text="Contact Name:", bg="#B3EFFF"),
            "name_entry": tk.Entry(root, bg="white"),
            "number_label": tk.Label(root, text="Phone Number:", bg="#B3EFFF"),
            "number_entry": tk.Entry(root, bg="white"),
            "new_ref_label": tk.Label(root, text="New Reference Number:", bg="#B3EFFF"),
            "new_ref_entry": tk.Entry(root, bg="white"),
            "submit_button": tk.Button(root, text="Submit", bg="#bbbbbb", fg="black"),
            "edit_name_btn": tk.Button(root, text="Edit Contact Name", width=25, command=self.edit_contact_name, bg="#bbbbbb", fg="black"),
            "edit_number_btn": tk.Button(root, text="Edit Contact Number", width=25, command=self.edit_contact_number, bg="#bbbbbb", fg="black"),
            "edit_ref_btn": tk.Button(root, text="Edit Reference Number", width=25, command=self.edit_contact_ref, bg="#bbbbbb", fg="black"),
            "edit_all_btn": tk.Button(root, text="Edit All", width=25, command=self.edit_contact_all, bg="#bbbbbb", fg="black"),
        }

        # To group main buttons
        self.button_frame = tk.Frame(root, bg="#B3EFFF")
        self.button_frame.pack(pady=10)

        # Buttons for main functions
        buttons = [
            ("Add New Contact", self.add_contact),
            ("Search Contact", self.search_contact),
            ("Edit Contact", self.edit_contact),
            ("Delete Contact", self.delete_contact),
            ("View All Contacts", self.view_contacts),
            ("Exit", self.confirm_exit),
        ]
        for text, cmd in buttons:
            tk.Button(self.button_frame, text=text, width=25, command=cmd, bg="#bbbbbb", fg="black").pack(pady=3)

        self.hide_all()  # Hide input widgets on menu and only pops up when called

    def update_display(self, text):
        # Updates the display area with provided text
        self.display.config(state="normal")
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, text)
        self.display.config(state="disabled")

    def get(self, key):
        # Returns the widget corresponding to the key
        return self.widgets[key]

    def hide_all(self):
        # Hides all input widgets
        for widget in self.widgets.values():
            widget.pack_forget()

    def clear_inputs(self):
        # Clears all entry fields
        self.get("ref_entry").delete(0, tk.END)
        self.get("name_entry").delete(0, tk.END)
        self.get("number_entry").delete(0, tk.END)
        self.get("new_ref_entry").delete(0, tk.END)

    def show_inputs(self, ref=False, name=False, number=False, new_ref=False, action=None, text="Submit"):
        # Show inputs when called
        self.hide_all()
        self.clear_inputs()
        if ref:
            self.get("ref_label").pack(pady=5)
            self.get("ref_entry").pack(pady=5)
        if new_ref:
            self.get("new_ref_label").pack(pady=5)
            self.get("new_ref_entry").pack(pady=5)
        if name:
            self.get("name_label").pack(pady=5)
            self.get("name_entry").pack(pady=5)
        if number:
            self.get("number_label").pack(pady=5)
            self.get("number_entry").pack(pady=5)

        self.get("submit_button").config(command=action, text=text)
        self.get("submit_button").pack(pady=5)

    def view_contacts(self):
        # Displays all stored contacts
        self.hide_all()
        if self.contacts:
            output = ""
            for ref, (name, num) in sorted(self.contacts.items()):
                output += f"Reference Number: {ref} |    Name: {name} |    Phone Number: {num}\n"
        else:
            output = "No contacts available."
        self.update_display(output)

    def add_contact(self):
        # Prepares input textbox for adding a new contact
        self.update_display("")
        self.get("ref_label").config(text="Reference Number:")
        self.get("name_label").config(text="Contact Name:")
        self.get("number_label").config(text="Contact Number:")
        self.show_inputs(ref=True, name=True, number=True, action=self.perform_add_contact, text="Add Contact")

    def perform_add_contact(self):
        # Adds a contact after validation
        ref = self.get("ref_entry").get().strip()
        name = self.get("name_entry").get().strip()
        number = self.get("number_entry").get().strip()

        if not (ref and name and number):
            return messagebox.showwarning("Input Error", "Please fill in all fields.")

        try:
            ref_int = int(ref)
        except ValueError:
            return messagebox.showwarning("Input Error", "Reference number must only consist of purely numbers.")
        if ref_int == 0:
            return messagebox.showwarning("Input Error", "Reference number cannot be 0.")
        if not number.isdigit() or len(number) != 11 or not number.startswith("09"):
            return messagebox.showwarning("Input Error", "Invalid phone number. Start with '09' and use 11 digits.")
        if ref_int in self.contacts:
            return messagebox.showwarning("Duplicate Error", f"Reference number {ref_int} already exists.")
        if any(existing_number == number for _, existing_number in self.contacts.values()):
            return messagebox.showwarning("Duplicate Error", f"Contact number {number} already exists.")

        self.contacts[ref_int] = (name, number)
        messagebox.showinfo("Success", "Contact added successfully.")
        self.view_contacts()

    def search_contact(self):
        # Prepares input for searching a contact
        self.update_display("")
        self.show_inputs(ref=True, action=self.perform_search_contact, text="Search Contact")

    def perform_search_contact(self):
        # Searches and displays contact by reference number
        ref = self.get("ref_entry").get().strip()
        try:
            ref_int = int(ref)
        except ValueError:
            return messagebox.showwarning("Input Error", "Reference number must only consist of purely numbers.")

        if ref_int in self.contacts:
            name, number = self.contacts[ref_int]
            output = f"Reference Number: {ref_int} |     Name: {name} |    Phone Number: {number}"
            self.update_display(output)
        else:
            messagebox.showwarning("Not Found", "Entered reference number is not found.")
            self.update_display("")

    def delete_contact(self):
        # Prepares input for deleting a contact
        self.update_display("")
        self.show_inputs(ref=True, action=self.perform_delete_contact, text="Delete Contact")

    def perform_delete_contact(self):
        # Deletes a contact by reference number
        ref = self.get("ref_entry").get().strip()
        try:
            ref_int = int(ref)
        except ValueError:
            return messagebox.showwarning("Input Error", "Reference number must only consist of purely numbers.")

        if ref_int in self.contacts:
            del self.contacts[ref_int]
            messagebox.showinfo("Success", "Contact deleted successfully.")
            self.view_contacts()
        else:
            messagebox.showwarning("Not Found", "Reference number not found.")

    def edit_contact(self):
        # Displays options for the 4 types of editing
        self.update_display("")
        self.hide_all()
        self.clear_inputs()
        self.get("edit_name_btn").pack(pady=2)
        self.get("edit_number_btn").pack(pady=2)
        self.get("edit_ref_btn").pack(pady=2)
        self.get("edit_all_btn").pack(pady=2)

    def edit_contact_name(self):
        # Prepare textbox to edit contact name
        self.edit_mode = "name"
        self.get("ref_label").config(text="Reference Number:")
        self.get("name_label").config(text="New Contact Name:")
        self.show_inputs(ref=True, name=True, action=self.perform_edit_contact, text="Update Contact")

    def edit_contact_number(self):
        # Prepare textbox to edit contact number
        self.edit_mode = "number"
        self.get("ref_label").config(text="Reference Number:")
        self.get("number_label").config(text="New Contact Number:")
        self.show_inputs(ref=True, number=True, action=self.perform_edit_contact, text="Update Contact")

    def edit_contact_ref(self):
        # Prepare textbox to edit reference number
        self.edit_mode = "ref"
        self.get("ref_label").config(text="Current Reference Number:")
        self.get("new_ref_label").config(text="New Reference Number:")
        self.show_inputs(ref=True, new_ref=True, action=self.perform_edit_contact, text="Update Contact")

    def edit_contact_all(self):
        # Prepare textbox to edit all fields
        self.edit_mode = "all"
        self.get("ref_label").config(text="Reference Number:")
        self.get("new_ref_label").config(text="New Reference Number:")
        self.get("name_label").config(text="New Contact Name:")
        self.get("number_label").config(text="New Phone Number:")
        self.show_inputs(ref=True, new_ref=True, name=True, number=True, action=self.perform_edit_contact, text="Update Contact")

    def perform_edit_contact(self):
        # Performs the actual update based on the selected edit mode
        ref = self.get("ref_entry").get().strip()
        try:
            ref_int = int(ref)
        except ValueError:
            return messagebox.showwarning("Input Error", "Reference number must only consist of purely numbers.")

        if ref_int not in self.contacts:
            return messagebox.showwarning("Not Found", "Reference number not found.")

        current_name, current_number = self.contacts[ref_int]

        if self.edit_mode == "name":
            # Edit name only
            new_name = self.get("name_entry").get().strip()
            if new_name == current_name:
                return messagebox.showinfo("No Change", "The contact name is unchanged.")
            if not new_name:
                return messagebox.showwarning("Input Error", "Enter a new name.")
            self.contacts[ref_int] = (new_name, current_number)

        elif self.edit_mode == "number":
            # Edit number only
            new_number = self.get("number_entry").get().strip()
            if new_number == current_number:
                return messagebox.showinfo("No Change", "The contact number is unchanged.")
            if not new_number.isdigit() or len(new_number) != 11 or not new_number.startswith("09"):
                return messagebox.showwarning("Input Error", "Invalid new phone number. Start with '09' and use 11 digits.")
            if any(existing_number == new_number and ref_int != existing_ref
                   for existing_ref, (_, existing_number) in self.contacts.items()):
                return messagebox.showwarning("Duplicate Error", "Phone number already exists.")
            self.contacts[ref_int] = (current_name, new_number)

        elif self.edit_mode == "ref":
            # Edit reference number
            new_ref = self.get("new_ref_entry").get().strip()
            try:
                new_ref_int = int(new_ref)
            except ValueError:
                return messagebox.showwarning("Input Error", "Reference number must only consist of purely numbers.")
            if new_ref_int == 0:
                return messagebox.showwarning("Input Error", "Reference number cannot be 0.")
            if new_ref_int in self.contacts:
                return messagebox.showwarning("Input Error", "New reference number already exists.")
            self.contacts[new_ref_int] = self.contacts.pop(ref_int)

        elif self.edit_mode == "all":
            # Edit reference, name, and number
            new_ref = self.get("new_ref_entry").get().strip()
            new_name = self.get("name_entry").get().strip()
            new_number = self.get("number_entry").get().strip()

            if new_ref == str(ref_int) and new_name == current_name and new_number == current_number:
                return messagebox.showinfo("No Change", "No changes were made to the contact details.")

            if not (new_ref and new_name and new_number):
                return messagebox.showwarning("Input Error", "Please fill in all fields.")
            try:
                new_ref_int = int(new_ref)
            except ValueError:
                return messagebox.showwarning("Input Error", "Reference number must only consist of purely numbers.")
            if new_ref_int == 0:
                return messagebox.showwarning("Input Error", "Reference number cannot be 0.")
            if not new_number.isdigit() or len(new_number) != 11 or not new_number.startswith("09"):
                return messagebox.showwarning("Input Error", "Invalid phone number. Start with '09' and use 11 digits.")
            if any(existing_number == new_number and ref_int != existing_ref
                   for existing_ref, (_, existing_number) in self.contacts.items()):
                return messagebox.showwarning("Duplicate Error", "Phone number already exists.")
            if new_ref_int != ref_int and new_ref_int in self.contacts:
                return messagebox.showwarning("Input Error", "New reference number already exists.")

            del self.contacts[ref_int]
            self.contacts[new_ref_int] = (new_name, new_number)

        messagebox.showinfo("Success", "Contact updated successfully.")
        self.view_contacts()

    def confirm_exit(self):
        # Confirm before exiting the system
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

#To run the system
if __name__ == "__main__":
    root = tk.Tk()
    ContactBook(root)
    root.mainloop()