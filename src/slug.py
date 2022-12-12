from src.replace import replace


class GithubSlugger:
    def __init__(self):
        self.reset()

    def reset(self):
        """Forget all previous slugs"""
        self.occurrences = dict()

    def slug(self, value: str, maintain_case: bool = False):
        """Generate a unique slug.

          Tracks previously generated slugs: repeated calls with the same value
          will result in different slugs.
          Use the `slug` function to get same slugs.

          Parameters:
          value (str): String of text to slugify
          maintain_case (bool): Keep the current case, otherwise make all
          lowercase

          Returns:
          str: A unique slug string
        """
        result = slug(value, maintain_case)
        original_slug = result
        count = self.occurrences.get(original_slug, 0)
        while self.occurrences.get(result, None) is not None:
            count += 1
            result = f'{original_slug}-{count}'

        self.occurrences[original_slug] = count
        self.occurrences[result] = 0
        return result


def slug(value: str, maintain_case: bool = False):
    """Generate a slug.

      Does not track previously generated slugs: repeated calls with the same
      value will result in the exact same slug.
      Use the `GithubSlugger` class to get unique slugs.

      Parameters:
      value (str): String of text to slugify
      maintain_case (bool): Keep the current case, otherwise make all lowercase

      Returns:
      str: A unique slug string
    """
    if type(value) != str:
        return ''

    if not maintain_case:
        value = value.lower()

    return replace(value)
