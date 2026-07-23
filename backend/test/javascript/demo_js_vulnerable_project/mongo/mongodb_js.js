// mongo/mongo_queries.ts

// 1. Celoten filter prihaja iz query parametra
export async function findMongoUser(req, users) {
    const userFilter = req.query.filter;

    const result = await users.find(userFilter);

    return result;
}


// 2. Celoten filter prihaja iz telesa zahtevka
export async function findMongoUserByBody(req, users) {
    const queryFilter = req.body.filter;

    const result = await users.findOne(queryFilter);

    return result;
}


// 3. Filter za brisanje prihaja neposredno od uporabnika
export async function deleteMongoUser(req, users) {
    const filterData = req.query.filter;

    const result = await users.deleteOne(filterData);

    return result;
}


// 4. Celotno telo zahtevka se neposredno uporabi kot MongoDB filter
export async function findUserDirectly(req, users) {
    return users.findOne(req.body);
}




// 5. Nezaupanja vreden filter pri posodabljanju
export async function updateMongoUser(req, users) {
    const filter = req.body.filter;
    const update = req.body.update;

    return users.updateOne(filter, update);
}

