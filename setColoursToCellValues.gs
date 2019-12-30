// Macro to use in Google Sheets for changing the fill colour of a cell
// to its current value.
//
// If you have a range of cells that contain colour values (e.g. hexadecimal colours),
// select the cells and then invoke this macro -- their fill colours will be
// updated to match their value!
//
// To use:
//
//   1. Inside a Google Sheets spreadsheet, select the menu bar item
//        Tools > Script Editor
//
//   2. In the Script Editor, select the menu bar item
//        File > New > Script file
//      Call it something like setColoursToCellValues.gs.
//
//   3. Copy/paste the code from this file into your new script file.
//      Select the menu bar item:
//        File > Save
//
//   4. Go back to your spreadsheet, select the menu bar item
//        Tools > Macros > Import
//      You'll be shown a list of files and functions.  Find the one named
//      "setColoursToCellValues", and click "Add Function".
//
//   5. Select the cells you want to set the fill colour of, then select
//      the menu bar item
//        Tools > Macros > setColoursToCellValues
//
// See the macro in action: https://twitter.com/alexwlchan/status/1211790869097046016
//

function setColoursToCellValues() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();

  // Get all the selections in the current spreadsheet.
  //
  // e.g. if you have selected the first ten rows of the first column,
  // this contains the range A1:A10.
  var ranges = sheet.getSelection().getActiveRangeList().getRanges();

  for (var rangeIndex = 0; rangeIndex < ranges.length; rangeIndex++) {
    var currentRange = ranges[rangeIndex];

    for (var row = 1; row <= currentRange.getNumRows(); row++) {
      for (var column = 1; column <= currentRange.getNumColumns(); column++) {

        // Looks for hexadecimal colour strings that are *not* preceded by
        // a leading hash, e.g. 00a123, ff0000, 00FFA1.
        //
        // When you call cell.setBackground(), if you pass a hex value it
        // wants a leading hash, so we need to add it.
        var regex = new RegExp("^[0-9a-fA-F]{6}$");

        var cell = currentRange.getCell(row, column);

        var color = cell.getValue();

        if (regex.exec(color) !== null) {
          color = "#" + color;
        }

        cell.setBackground(color);
      }
    }
  }
}
