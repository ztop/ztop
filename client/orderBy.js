/**
 * orderBy filter for PolymerExpressions
 *
 * See http://docs.angularjs.org/api/ng.filter:orderBy
 * Notes:
 *  * No support for function predicates
 *  * "+" prefix not supported in predicate strings because it's redundant
 */

(function() {
  PolymerExpressions.prototype.orderBy = function(data, columnsToOrderBy, reverse) {
    // Sorting with maps, ala
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort#Sorting_maps

    var reverseSortValues = [];

    columnsToOrderBy.forEach(function(element, index) {
      if (element[0] == '-') {
        columnsToOrderBy[index] = element.substr(1);
        reverseSortValues.push(true);
      }
      else {
        reverseSortValues.push(false);
      }
    });

    // temporary holder of position and sort-values
    var map = data.map(function(element, index){
      var sortValues = columnsToOrderBy.map(function(key) {
        return element[key];
      });

      return {
        index: index,
        sortValues: sortValues
      };
    });

    // sorting the map containing the reduced values
    map.sort(function (a, b) {
      var length = a.sortValues.length;

      for (var i = 0; i < length; i++) {
        if (reverseSortValues[i] == false) {
          if (a.sortValues[i] < b.sortValues[i])
            return -1;
          else if (a.sortValues[i] > b.sortValues[i])
            return 1;
        }
        else {
          if (a.sortValues[i] > b.sortValues[i])
            return -1;
          else if (a.sortValues[i] < b.sortValues[i])
            return 1;
        }
      }

      return 0;
    });

    if (reverse === true) {
      map.reverse();
    }

    // container for the resulting order
    var result = map.map(function(element) {
      return data[element.index];
    });

    return result;
  };
})();
