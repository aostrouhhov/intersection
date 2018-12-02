# Intersection of a Free Grammar and a Graph

## Branches
There are 2 branches. `master` branch keeps simple algorithm implementation on `NumPy` arrays. `cuda` branch keeps the same algorithm using `CuPy` library instead of `NumPy`.

## Algorithm
Each nonterm has its own bool matrix. At the begining 'True' in '(i,j) means that term in Graph which stands between veritces 'i' and 'j' is producable from this nonterm.

Go through all grammar transitions multiple times. For each transition of view 'A -> B C' do the following: A = A + B * C. Continue loop while nonterm matrices change. Stop when matrices stop changing.

Answer can be presented as matrix with list of nonterms in each cell (nonterm in (i,j) means that nonterm matrix has 'True' in (i,j)). Or just as file with all nonterms and (i,j)'s where concrete nonterm's matrix has 'True'.

## Rules
Use: `python3 inter.py grammar_file graph_file answer_file`

Contex-Free grammar should be defined in Chomsky Normal Form. Transitions look as follows:

    nonterm nonterm nonterm
    nonterm term
    ...

Indexing in Graph should be defined in numerical sequence starting from 0. Graph should be defined by its edges:

    from term to
    ...

Answer is presented in file with all nonterms and indexes of their matrices. Write only theose indexes in which matrix value is 'True':

    nonterm1 i j ...
    nonterm2
    nonterm3 i j m n       # means that nonterm3_matrix[i][j] == True
    ...                    # and nonterm3_matrix[m][n] == True
