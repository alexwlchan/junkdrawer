// The expected format of a spending
// entry is a three-line draft:
//
//     (amount)
//     (tags, space separated)
//     (description, may be multi-line)
//
components = draft
  .content
  .split("\n", limit = 3);

if (components.length !== 3) {
  alert("Not enough lines in the budget!");
  stopAction();
}

// Build the JSON blob which is to be
// stored in Dropbox.
amount = parseFloat(components[0]);
tags = components[1]
  .toLowerCase()
  .split(" ")
  .sort();
description = components[2];

date_created = draft.createdDate;

data = {
  "amount": amount,
  "tags": tags,
  "description": description,
  "date_created": date_created,
}

draft.content = JSON.stringify(
  data, replace = null, space = 2
);
commit(draft);
