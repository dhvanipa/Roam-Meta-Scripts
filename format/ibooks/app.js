function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);

    document.getElementById("successMessage").style.visibility = "visible";
}

function isDate(date) {
    return (new Date(date) !== "Invalid Date") && !isNaN(new Date(date));
}

function strEqual(str1, str2) {
    return str1.localeCompare(str2) === 0;
}

function formatHighlights() {
    var rawText = document.getElementById("inputText").value;
    var rawTextArray = rawText.split("\n");

    var output = ""

    var currentChapter = "";
    var currentChapterBullets = "";

    var i = 0;
    while (i < rawTextArray.length) {
        var line = rawTextArray[i];
        if (isDate(line)) {
            var newChapter = rawTextArray[i + 1];
            if (currentChapter.length == 0) {
                currentChapter = newChapter;
                currentChapterBullets += rawTextArray[i + 2] + "\n"
            } else if (strEqual(newChapter, currentChapter)) {
                currentChapterBullets += rawTextArray[i + 2] + "\n"
            } else {
                // console.log(currentChapter);
                // console.log(currentChapterBullets);
                // console.log("------------------\n\n")
                output += currentChapter + "\n";
                output += currentChapterBullets + "\n";
                output += "------------------\n\n"
                currentChapter = newChapter;
                currentChapterBullets = rawTextArray[i + 2] + "\n";
            }
            i += 2;
        }
        i++;
    }
    output += currentChapter + "\n";
    output += currentChapterBullets + "\n";
    output += "------------------\n\n"

    download("output.txt", output);
}

function hideSuccess() {
    document.getElementById("successMessage").style.visibility = "hidden";
}

function loadSample() {
    fetch('zero-to-one.txt')
    .then(response => response.text())
    .then(text => document.getElementById("inputText").value = text);
}

document.getElementById("inputText").addEventListener('input', hideSuccess);