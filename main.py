import time
import json
import os
import requests

class RememberMe:
    def __init__(self):
        self.reminders = []
        self.file_name = "reminders.json"
        self.load_reminders()
        self.webhook_url = "[url]"  # Remplacez par votre URL de webhook Discord

    def display_main_menu(self):
        print("\n--- Menu Principal ---")
        print("1. Ajouter un rappel")
        print("2. Afficher les rappels")
        print("3. Marquer un rappel comme terminé")
        print("4. Supprimer un rappel")
        print("5. Envoyer rappels à Discord")
        print("6. Quitter")

    def add_reminder(self):
        print("\n--- Ajouter un Rappel ---")
        title = input("Titre : ")
        description = input("Description : ")
        if title and description:
            reminder = {"title": title, "description": description, "status": "À faire"}
            self.reminders.append(reminder)
            self.save_reminders()
            print("Rappel ajouté avec succès !")
        else:
            print("Le titre et la description sont nécessaires.")

    def display_reminders(self):
        print("\n--- Liste des Rappels ---")
        if not self.reminders:
            print("Aucun rappel à afficher.")
        else:
            for idx, reminder in enumerate(self.reminders, start=1):
                print(f"{idx}. {reminder['title']} - {reminder['description']} ({reminder['status']})")

    def mark_done(self):
        print("\n--- Marquer un Rappel comme Terminé ---")
        self.display_reminders()
        if self.reminders:
            try:
                choice = int(input("Entrez le numéro du rappel à marquer comme terminé : "))
                if 1 <= choice <= len(self.reminders):
                    self.reminders[choice - 1]["status"] = "Terminé"
                    self.save_reminders()
                    print("Rappel marqué comme terminé.")
                else:
                    print("Numéro invalide.")
            except ValueError:
                print("Entrée invalide.")

    def delete_reminder(self):
        print("\n--- Supprimer un Rappel ---")
        self.display_reminders()
        if self.reminders:
            try:
                choice = int(input("Entrez le numéro du rappel à supprimer : "))
                if 1 <= choice <= len(self.reminders):
                    del self.reminders[choice - 1]
                    self.save_reminders()
                    print("Rappel supprimé.")
                else:
                    print("Numéro invalide.")
            except ValueError:
                print("Entrée invalide.")

    def save_reminders(self):
        """Sauvegarde les rappels dans un fichier JSON."""
        with open(self.file_name, "w") as file:
            json.dump(self.reminders, file, indent=4)
    
    def load_reminders(self):
        """Charge les rappels depuis le fichier JSON, s'il existe."""
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                self.reminders = json.load(file)
        else:
            self.reminders = []

    def send_to_discord(self):
        """Envoie les rappels à un webhook Discord."""
        if not self.reminders:
            print("Aucun rappel à envoyer.")
            return

        message = "**Liste des Rappels :**\n"
        for reminder in self.reminders:
            message += f"- **{reminder['title']}** : {reminder['description']} (Status: {reminder['status']})\n"
        
        # Structure du payload pour Discord
        data = {
            "content": message
        }

        try:
            response = requests.post(self.webhook_url, json=data)
            if response.status_code == 200:
                print("Rappels envoyés avec succès à Discord.")
            else:
                print(f"Erreur lors de l'envoi : {response.status_code}")
        except Exception as e:
            print(f"Erreur de connexion au Webhook : {e}")

    def run(self):
        while True:
            self.display_main_menu()
            choice = input("\nEntrez votre choix : ")

            if choice == "1":
                self.add_reminder()
            elif choice == "2":
                self.display_reminders()
            elif choice == "3":
                self.mark_done()
            elif choice == "4":
                self.delete_reminder()
            elif choice == "5":
                self.send_to_discord()
            elif choice == "6":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Essayez à nouveau.")

if __name__ == "__main__":
    app = RememberMe()
    app.run()
