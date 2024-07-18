class NFA:
    def __init__(self):
        self.states = set() 
        self.start_state = ""  
        self.final_states = set()  
        self.delt = {}  # Dictionary to store transitions in the form {from_state: {symbol: {next_states}}}

    def add_transition(self, from_state, to_state, symbol):
        if from_state not in self.delt:#if there is not any key as from_state add it
            self.delt[from_state] = {}
        if symbol not in self.delt[from_state]:#if there is not any key as from_state and symbol add it
            self.delt[from_state][symbol] = set()
        self.delt[from_state][symbol].add(to_state) # Adds a transition from `from_state` to `to_state` on `symbol`

    def get_transitions(self):
        delt = []
        for from_state, paths in self.delt.items():
            for symbol, to_states in paths.items():
                for to_state in to_states:
                    delt.append((from_state, symbol, to_state))
        return delt

def create_state(state_num): #creates states with name qi
    state = f"q{state_num}"
    return state

state_num = 0  
regex = input("enter RE: ") 

sigma = set()  # alphabet used in the re
for i in regex:
    if i.isalpha():
        sigma.add(i)  
nfa = NFA()  

stack_parenthesis = []  # Stack to handle() 
now = create_state(state_num)#Track the current state
state_num += 1  
nfa.states.add(now) 
nfa.start_state = now  
last = now  #Track the previous state
plus_stack = []  # Stack to handle '+' operations
plus_stack1 = []

for i in range(0, len(regex)):
    if regex[i] == '*':
        continue  # Skip '*' as it is handled in the next iteration(*is after symbol or after parenthesis)

    if regex[i] == '+': #baa+b
        new = create_state(state_num)
        state_num += 1
        nfa.states.add(new)
        if len(stack_parenthesis):
            plus_stack.append(last)
            nfa.add_transition(stack_parenthesis[-1], new, 'λ')  # Add λ transition from a to new state
        else:
            plus_stack1.append(last)
            nfa.add_transition(nfa.start_state, new, 'λ')
        last = new

    elif regex[i] == '(':
        stack_parenthesis.append(last)  # Push the previous state onto the stack

    elif regex[i] == ')':
        # Handle closing parenthesis
        start = stack_parenthesis.pop()  # Pop the state before '(' from the stack
        new = create_state(state_num)
        state_num += 1
        nfa.states.add(new)
        plus_stack.append(last)
        for j in plus_stack:
            nfa.add_transition(j, new, 'λ')  # Add λ transitions
        plus_stack.clear()

        if (i + 1 < len(regex) and regex[i + 1] == '*'):
            # Add transitions for '*' closure (λ transitions from last to start and from start to last)
            nfa.add_transition(new, start, 'λ')
            nfa.add_transition(start, new, 'λ')
        last = new

    else:
        # Handle regular characters
        if (i + 1 < len(regex) and regex[i + 1] == '*'):
            # Add transition for character with '*' closure
            nfa.add_transition(last, last, regex[i])
        else:
            # Add transition for normal character
            new = create_state(state_num)
            state_num += 1
            nfa.states.add(new)
            nfa.add_transition(last, new, regex[i])
            last = new

new = create_state(state_num)
state_num += 1
nfa.states.add(new)
nfa.final_states.add(new)

nfa.add_transition(last, new, 'λ')
for i in plus_stack1:
    nfa.add_transition(i, new, 'λ')

print(' '.join(sigma))
print(' '.join(nfa.states))
print(nfa.start_state)
print(' '.join(list(nfa.final_states)))

for from_state, transitions in nfa.delt.items():
    for symbol, to_states in transitions.items():
        for to_state in to_states:
            print(f"{from_state} {symbol} {to_state}")