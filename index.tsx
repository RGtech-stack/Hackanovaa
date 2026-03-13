import { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

export default function HomeScreen() {
  const [selectedAction, setSelectedAction] = useState<"need" | "provide" | null>(null);
  const selectedLabel = selectedAction === "need" ? "Need Help" : "Provide Help";

  return (
    <View style={styles.container}>
      <View style={styles.contentCard}>
        <Text style={styles.subtitle}>
          {selectedAction ? `${selectedLabel}: choose assistance type.` : "Select your role to continue."}
        </Text>

        {!selectedAction && (
          <View style={styles.actionsContainer}>
            <TouchableOpacity style={[styles.primaryButton, styles.firstScreenButton]} onPress={() => setSelectedAction("need")}>
              <Text style={styles.buttonText}>I Need Help</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.secondaryButton, styles.firstScreenButton]} onPress={() => setSelectedAction("provide")}>
              <Text style={styles.buttonText}>I Provide Help</Text>
            </TouchableOpacity>
          </View>
        )}

        {selectedAction && (
          <View style={styles.optionsContainer}>
            <TouchableOpacity style={[styles.primaryButton, styles.firstScreenButton]}>
              <Text style={styles.buttonText}>Food</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.secondaryButton, styles.firstScreenButton]}>
              <Text style={styles.buttonText}>Medicine</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.primaryButton, styles.firstScreenButton]}>
              <Text style={styles.buttonText}>Rescue</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#000000",
    paddingHorizontal: 18,
    position: "relative"
  },

  contentCard: {
    width: "100%",
    maxWidth: 420,
    borderRadius: 26,
    paddingVertical: 28,
    paddingHorizontal: 20,
    backgroundColor: "#0f0f0f"
  },

  subtitle: {
    color: "#f2f2f2",
    fontSize: 16,
    marginBottom: 22
  },

  actionsContainer: {
    gap: 12
  },

  primaryButton: {
    width: "100%",
    paddingVertical: 16,
    backgroundColor: "#ffffff",
    borderRadius: 999,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 4
  },

  secondaryButton: {
    width: "100%",
    paddingVertical: 16,
    backgroundColor: "#d9d9d9",
    borderRadius: 999,
    alignItems: "center"
  },

  firstScreenButton: {
    backgroundColor: "#ffb3b3"
  },

  optionsContainer: {
    marginTop: 8,
    gap: 12
  },

  buttonText: {
    color: "#000000",
    fontSize: 18,
    fontWeight: "bold"
  }
});