export async function findMongoUser(req: any, users: any) {
  const filter = req.body.filter;
  const operator = req.query.operator;
  return users.findOne({ name: filter, enabled: { $ne: operator } });
}
