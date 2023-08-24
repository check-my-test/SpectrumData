
var db = db.getSiblingDB('parser_db');

db.createCollection("htmls")

var indexExists = db.htmls.getIndexes().some(function(index) {
    return index.name === 'url_1';
});

if (!indexExists) {
    db.htmls.createIndex({ 'url': 1 }, { unique: true });
    print('Индекс по полю "url" был успешно создан.');
} else {
    print('Индекс по полю "url" уже существует.');
}
