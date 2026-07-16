def build_citations(results):

    """
    Vytvorí zoznam citácií z výsledkov retrievera.
    """

    lines = []

    lines.append("")

    lines.append("Sources")
    lines.append("-------")

    used = set()

    for result in results:

        key = (

            result.author,

            result.book,

            result.page

        )

        if key in used:

            continue

        used.add(key)

        lines.append(

            f"- {result.author}, "
            f"{result.book}, "
            f"page {result.page}"

        )

    return "\n".join(lines)