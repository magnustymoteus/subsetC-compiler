.text
#.globl printf

 printf:
    sw $fp, 0($sp)  #new stack frame
    move $fp, $sp
    sw $ra, -4($fp)

    lw $t5, 4($fp)
    mul $t5, $t5, 4
    add $t5, $t5, $fp

    addi $t7, $t5, 4

    lw $t7, 0($t7)

    li $t9, 1

    j print_loop


print_loop:
    lb $t3, 0($t7)       # Load byte from format string
    beq $t3, $zero, end_print  # If null character, end loop

    beq $t3, '%', handle_format  # If '%', handle format

    # Otherwise, print the character
    li $v0, 11            # Print character syscall
    move $a0, $t3
    syscall

    addi $t7, $t7, 1      # Move to next character
    j print_loop



handle_format:

    addi $t7, $t7, 1      # Move to next character to check format specifier
    lb $t3, 0($t7)        # Load the format specifier

    move $a0, $t3
    move $v1, $t6
    jal is_digit
    beq $t6, 1, handle_padding
    beq $v1, 1, apply_padding

check_format:
    li $t9, 0
    li $t4, 0
    beq $t3, 's', print_string  # If 's', print string
    beq $t3, 'd', print_integer # If 'd', print integer
    beq $t3, 'f', print_float
    beq $t3, 'c', print_character
    beq $t3, 'x', print_hex


    # If unknown specifier, just print it as is
    li $v0, 11            # Print character syscall
    move $a0, $t3         # Print the specifier
    syscall
    addi $t7, $t7, 1      # Move to next character
    j print_loop


is_digit:
    sge $t0, $a0, 48
    sle $t1, $a0, 57
    and $t6, $t0, $t1
    jr $ra

handle_padding:
    andi $t8,$t3,0x0F
    mul $t4, $t4, 10
    add $t4, $t4, $t8

    j handle_format

apply_padding:
    li $a0, 32
    li $v0, 11
    syscall

    addi $t4, $t4, -1
    beqz $t4, check_format
    j apply_padding

print_string:
    lw $t2, 0($t5)
    # Print the string pointed to by $t1
    move $a0, $t2
    li $v0, 4            # Print string syscall
    syscall

    addi $t7, $t7, 1      # Move to next character
    addi $t5, $t5, -4
    j print_loop

print_integer:
    lw $t2, 0($t5)
    # Print the integer in $t2
    move $a0, $t2
    li $v0, 1             # Print integer syscall
    syscall

    addi $t7, $t7, 1      # Move to next character
    addi $t5, $t5, -4
    j print_loop

print_float:
    lwc1 $f12, 0($t5)
    li $v0, 2
    syscall

    addi $t7, $t7, 1
    addi $t5, $t5, -4
    j print_loop
print_character:
    lb $t2, 0($t5)
    # Print the character in $t2
    move $a0, $t2
    li $v0, 11             # Print character syscall
    syscall

    addi $t7, $t7, 1      # Move to next character
    addi $t5, $t5, -4
    j print_loop
print_hex:
    lw $t2, 0($t5)
    # Print the integer in $t2
    move $a0, $t2
    li $v0, 34           # Print integer syscall
    syscall

    addi $t7, $t7, 1      # Move to next character
    addi $t5, $t5, -4
    j print_loop
end_print:
# clean up stack frame
    lw $ra, -4($fp)
    move $sp, $fp
    lw $t5, 4($fp)
    addiu $t5, $t5, 1
    mul $t5, $t5, 4
    lw $fp, 0($sp)
    addu $sp, $sp, $t5
    jr $ra



