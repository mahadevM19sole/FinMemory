from memory import FinMemory


memory = FinMemory()


memory.remember("salary", "₹60,000")
memory.remember("monthly_savings_goal", "₹15,000")
memory.remember("risk_appetite", "low")


print("Saved memories:")
print(memory.get_profile())


print("\nRecall savings goal:")
print(memory.recall("monthly_savings_goal"))