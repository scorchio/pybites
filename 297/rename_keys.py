from typing import Dict, Any, Collection, Sequence


def rename_keys(data: Dict[Any, Any]) -> Dict[Any, Any]:
    def _process_elem(elem):
        if not isinstance(elem, list) and not isinstance(elem, dict):
            return elem
        
        if isinstance(elem, list):
            return [_process_elem(value) for value in elem]

        if isinstance(elem, dict):
            results = {}
            for key, value in elem.items():
                if isinstance(key, str) and '@' == key[0]:
                    key = key[1:]
                results[key] = _process_elem(value)
            return results

    return _process_elem(data)