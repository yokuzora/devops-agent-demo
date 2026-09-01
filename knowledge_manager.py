from database import add_error_rule


def add_new_rule(

    keyword,

    category,

    root_cause,

    suggestions

):

    add_error_rule(

        keyword,

        category,

        root_cause,

        suggestions

    )
