import json
import os
from github_slugger import GithubSlugger, slug

dirname = os.path.dirname(__file__)

with open(f'{dirname}/fixtures.json', encoding='utf-8') as file:
    fixtures = json.load(file)


def test_basic():
    slugger = GithubSlugger()

    assert slugger.slug(1) == '', 'should return empty string for non-strings'

    assert slugger.slug('fooCamelCase', True) == 'fooCamelCase', 'should support `maintainCase`'  # foocamelcase
    assert slugger.slug('fooCamelCase') == 'foocamelcase', 'should support `maintainCase` (reference)'  # foocamelcase-1'

    assert slugger.slug('asd') == 'asd', 'should slug'
    assert slugger.slug('asd') == 'asd-1', 'should create unique slugs for repeated values'
    assert slugger.slug('asd') == 'asd-2', 'should create unique ever incrementing slugs for repeated values'
    assert slugger.slug('asd-3') == 'asd-3', 'should keep regular values'
    assert slugger.slug('asd-1') == 'asd-1-1', 'should consider previous depthened slugs'


def test_static_method():
    assert slug('foo') == 'foo', 'should slug'
    assert slug('foo') == 'foo', 'should create same slugs for repeated values'


def test_fixtures():
    slugger = GithubSlugger()

    count = 0
    for d in fixtures:
        name = d.get('name')
        input = d.get('input')
        expected = d.get('expected')
        assert slugger.slug(input) == expected, f'#{count}: {name}'
        count += 1
