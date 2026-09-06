# extract_configuration_param

Source: inspect: llama_cloud.types.ExtractConfigurationParam @ 2.15.0
Probed: 2026-09-01

## Signature

```
<TypedDict; see annotations and help below>
```

## Annotations

```
data_schema: ForwardRef('Required[Dict[str, Union[Dict[str, object], Iterable[object], str, float, bool, None]]]', module='llama_cloud.types.extract_configuration_param')
cite_sources: ForwardRef('bool', module='llama_cloud.types.extract_configuration_param')
confidence_scores: ForwardRef('bool', module='llama_cloud.types.extract_configuration_param')
disable_cache: ForwardRef('bool', module='llama_cloud.types.extract_configuration_param')
extraction_target: ForwardRef("Literal['per_doc', 'per_page', 'per_table_row']", module='llama_cloud.types.extract_configuration_param')
max_pages: ForwardRef('Optional[int]', module='llama_cloud.types.extract_configuration_param')
parse_config_id: ForwardRef('Optional[str]', module='llama_cloud.types.extract_configuration_param')
parse_tier: ForwardRef('Optional[str]', module='llama_cloud.types.extract_configuration_param')
sheet_names: ForwardRef('Optional[SequenceNotStr[str]]', module='llama_cloud.types.extract_configuration_param')
spreadsheet_mode: ForwardRef('bool', module='llama_cloud.types.extract_configuration_param')
system_prompt: ForwardRef('Optional[str]', module='llama_cloud.types.extract_configuration_param')
target_pages: ForwardRef('Optional[str]', module='llama_cloud.types.extract_configuration_param')
tier: ForwardRef("Literal['agentic', 'agentic_plus', 'cost_effective', 'turbo']", module='llama_cloud.types.extract_configuration_param')
version: ForwardRef('str', module='llama_cloud.types.extract_configuration_param')
```

## help()

```
Python Library Documentation: class ExtractConfigurationParam in module llama_cloud.types.extract_configuration_param

class ExtractConfigurationParam(builtins.dict)
 |  Extract configuration combining parse and extract settings.
 |
 |  Method resolution order:
 |      ExtractConfigurationParam
 |      builtins.dict
 |      builtins.object
 |
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables
 |
 |  __weakref__
 |      list of weak references to the object
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |
 |  __annotations__ = {'cite_sources': ForwardRef('bool', module='llama_cl...
 |
 |  __closed__ = None
 |
 |  __extra_items__ = typing_extensions.NoExtraItems
 |
 |  __mutable_keys__ = frozenset({'cite_sources', 'confidence_scores', 'da...
 |
 |  __optional_keys__ = frozenset({'cite_sources', 'confidence_scores', 'd...
 |
 |  __orig_bases__ = (typing_extensions.TypedDict,)
 |
 |  __readonly_keys__ = frozenset()
 |
 |  __required_keys__ = frozenset()
 |
 |  __total__ = False
 |
 |  ----------------------------------------------------------------------
 |  Methods inherited from builtins.dict:
 |
 |  __contains__(self, key, /)
 |      True if the dictionary has the specified key, else False.
 |
 |  __delitem__(self, key, /)
 |      Delete self[key].
 |
 |  __eq__(self, value, /)
 |      Return self==value.
 |
 |  __ge__(self, value, /)
 |      Return self>=value.
 |
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |
 |  __getitem__(self, key, /)
 |      Return self[key].
 |
 |  __gt__(self, value, /)
 |      Return self>value.
 |
 |  __init__(self, /, *args, **kwargs)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  __ior__(self, value, /)
 |      Return self|=value.
 |
 |  __iter__(self, /)
 |      Implement iter(self).
 |
 |  __le__(self, value, /)
 |      Return self<=value.
 |
 |  __len__(self, /)
 |      Return len(self).
 |
 |  __lt__(self, value, /)
 |      Return self<value.
 |
 |  __ne__(self, value, /)
 |      Return self!=value.
 |
 |  __or__(self, value, /)
 |      Return self|value.
 |
 |  __repr__(self, /)
 |      Return repr(self).
 |
 |  __reversed__(self, /)
 |      Return a reverse iterator over the dict keys.
 |
 |  __ror__(self, value, /)
 |      Return value|self.
 |
 |  __setitem__(self, key, value, /)
 |      Set self[key] to value.
 |
 |  __sizeof__(...)
 |      D.__sizeof__() -> size of D in memory, in bytes
 |
 |  clear(...)
 |      D.clear() -> None.  Remove all items from D.
 |
 |  copy(...)
 |      D.copy() -> a shallow copy of D
 |
 |  get(self, key, default=None, /)
 |      Return the value for key if key is in the dictionary, else default.
 |
 |  items(...)
 |      D.items() -> a set-like object providing a view on D's items
 |
 |  keys(...)
 |      D.keys() -> a set-like object providing a view on D's keys
 |
 |  pop(...)
 |      D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
 |
 |      If the key is not found, return the default if given; otherwise,
 |      raise a KeyError.
 |
 |  popitem(self, /)
 |      Remove and return a (key, value) pair as a 2-tuple.
 |
 |      Pairs are returned in LIFO (last-in, first-out) order.
 |      Raises KeyError if the dict is empty.
 |
 |  setdefault(self, key, default=None, /)
 |      Insert key with a value of default if key is not in the dictionary.
 |
 |      Return the value for key if key is in the dictionary, else default.
 |
 |  update(...)
 |      D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.
 |      If E is present and has a .keys() method, then does:  for k in E.keys(): D[k] = E[k]
 |      If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
 |      In either case, this is followed by: for k in F:  D[k] = F[k]
 |
 |  values(...)
 |      D.values() -> an object providing a view on D's values
 |
 |  ----------------------------------------------------------------------
 |  Class methods inherited from builtins.dict:
 |
 |  __class_getitem__(...)
 |      See PEP 585
 |
 |  fromkeys(iterable, value=None, /)
 |      Create a new dictionary with keys from iterable and values set to value.
 |
 |  ----------------------------------------------------------------------
 |  Static methods inherited from builtins.dict:
 |
 |  __new__(*args, **kwargs) class method of builtins.dict
 |      Create and return a new object.  See help(type) for accurate signature.
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes inherited from builtins.dict:
 |
 |  __hash__ = None

```

## Usage

- **Call:** Pass this mapping as `configuration` to `client.extract.run`.
- **Don't call:** Do not pass v1-only fields absent from these annotations.
- **Trap:** `target_pages` is the installed v2 page-window control; `num_pages_context` is not supported in SDK 2.15.0.
- **Returns:** The mapping configures the Extract job; `run` returns an `ExtractV2Job`.
