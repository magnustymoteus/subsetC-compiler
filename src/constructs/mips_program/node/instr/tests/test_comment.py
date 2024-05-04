from src.constructs.mips_program.node.instr import Comment


def test_comment():
    comment = Comment("This is a comment")
    assert str(comment) == "# This is a comment"
