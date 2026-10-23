import assert from "node:assert/strict";
import test from "node:test";
import { getPasswordStatus, validateEmail } from "../src/utils/validation.js";

test("password strength checks all five requirements", () => {
  assert.equal(getPasswordStatus("Abcdef1!").isValid, true);
  assert.equal(getPasswordStatus("abcdef1!").requirements[1].met, false);
  assert.equal(getPasswordStatus("ABCDEFG1!").requirements[2].met, false);
  assert.equal(getPasswordStatus("Abcdefgh!").requirements[3].met, false);
  assert.equal(getPasswordStatus("Abcdefg1").requirements[4].met, false);
  assert.equal(getPasswordStatus("Ab1!").requirements[0].met, false);
  assert.equal(
    getPasswordStatus("A".repeat(126) + "a1!").requirements[0].met,
    false,
  );
});

test("email validation rejects empty, malformed, and whitespace input", () => {
  assert.equal(validateEmail(""), false);
  assert.equal(validateEmail("not-an-email"), false);
  assert.equal(validateEmail("name @example.com"), false);
  assert.equal(validateEmail("person@example.com"), true);
});
