# LogicDesymplifier
Python application that converts logic statements using standard equivalence rules

Running the Application
-----------------------

The application can be started by using the executable named 'desymplifier' in the /dist/ directory

Usage
-----

**Input**

The application interface supplies 3 input boxes. 

  * Sentence: this is where you put the sentence you wish to desymplify
  * Iterations: this is the number of loops the application will run. That is, if iterations is 2, it will take the initial sentence provided and run it through all equivalences. Then for the second iteration, it will take all results from the first iteration, and run each one through all equivalences again.
  * Steps per iteration: this is the number of equivalences applied to the sentence per iteration. The software will attempt to apply an equivalence rule to every subsentence and atom in a single sentence before it returns the result. This input will limit the number applied before returning the result.
  
**Keyboard to Logic Symbol Key**

* ¬ = ~
* ∧ = &
* ∨ = |
* → = $

The software currently only supports single letter naming and negation, boolean, and conditional operators.
