""" Datele de intrare vor fi:

q0                          <- starea initiala
qAccept                     <- starea finala
q0,0,qRight0,_,>            <- o deplasare: separate prin ',' avem: starea actuala, caracterul de pe banda, noua stare, ce scrie pe banda (_ inseamna caracterul gol/vid), >/</_ este deplasarea)
qRight0,0,qRight0,0,>
qRight0,1,qRight0,1,>
q0,1,qRight1,_,>
qRight1,0,qRight1,0,>
qRight1,1,qRight1,1,>
qRight0,_,qSearch0L,_,<
qSearch0L,0,q1,_,<
qRight1,_,qSearch1L,_,<
qSearch1L,1,q1,_,<
q1,0,qLeft0,_,<
qLeft0,0,qLeft0,0,<
qLeft0,1,qLeft0,1,<
q1,1,qLeft1,_,<
qLeft1,0,qLeft1,0,<
qLeft1,1,qLeft1,1,<
qLeft0,_,qSearch0R,_,>
qSearch0R,0,q0,_,>
qLeft1,_,qSearch1R,_,>
qSearch1R,1,q0,_,>
qSearch0R,1,qReject,1,-
qSearch1R,0,qReject,0,-
qSearch0L,1,qReject,1,-
qSearch1L,0,qReject,0,-
q0,_,qAccept,_,-
q1,_,qAccept,_,-
qSearch0L,_,qAccept,_,-
qSearch0R,_,qAccept,_,-
qSearch1L,_,qAccept,_,-
qSearch1R,_,qAccept,_,-

"""

# TODO iar programul ar trebui sa citeasca datele si dupa oricate cuvinte diferite si sa afiseze
#   daca sunt validate sau nu. Spre exemplu:
"""

Ati citit masina Turing cu configurarea ... (si sa afisati datele citite aici)
Puteti introduce cuvinte pe care sa le testeze MT :).

cuvant: 0110
OK
cuvant: 001
not OK..
cuvant: 11100110111
OK
cuvant: 01
not OK..

"""

# TODO me: make a configuration that uses left side of the tape
# sa impart punctaj inre assignemnturile deja puse?

# input reading and sanitizing

f = open("input.txt", "rt")

data = f.read().split("\n")
intialState = data[0]
finalState = data[1]
transitions = {}

# transitions {()}
# will be represented in memory as a
# dictionary with a tuple as key ( startS, input_letter )
# and a list of 3-tuples as value ( endtS, write_on_tape, move_on_tape )

for i in range(2, len(data)):
    line = data[i].split(",")
    startS = line[0]
    tapeRead = line[1]
    endtS = line[2]
    write_on_tape = line[3]
    move_on_tape = line[4]

    if (startS, tapeRead) not in transitions:
        transitions[(startS, tapeRead)] = []
    transitions[(startS, tapeRead)].append((endtS, write_on_tape, move_on_tape))

head = 0
tape = []


def Write(c):
    global tape
    global head
    if head >= len(tape):
        tape.append('_')
    tape[head] = c

def Read():
    global tape
    global head
    if head >= len(tape):
        tape.append('_')
    return tape[head]

def Step(currentState):
    global accepted
    global finalState
    global head
    global tape

    if currentState == finalState:
        accepted = True
    if accepted: return

    if (currentState, Read()) in transitions:
        for tr in transitions[(currentState, Read())]:
            save_current = head
            save_tape = tape

            next_state = tr[0]
            Write(tr[1])
            
            #move head
            if tr[2] == '<':
                head -= 1
            if tr[2] == '>':
                head += 1
            Step(next_state)
            head = save_current
            tape = save_tape

if __name__ == "__main__":
    while True:
        word = input("cuvant: ")
        if word == "exit":
            break
        accepted = False
        head = 0
        tape = [w for w in word]
        Step(intialState)
        if accepted:
            print("accepted")
        else:
            print("rejected")