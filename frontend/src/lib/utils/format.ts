
export function truncateFrom(
  input: string,
  position: "start" | "end" | "middle",
  replacement: string,
  len: number
): string {
  if (input.length <= len) return input;

  const replacementLength = replacement.length;

  // Adjust length for the replacement text
  const allowedLength = len - replacementLength;

  if (allowedLength <= 0) {
    throw new Error("Replacement text is too long for the desired length.");
  }

  let startSliceEnd: number;
  let endSliceStart: number;

  switch (position) {
    case "start":
      startSliceEnd = 0;
      endSliceStart = input.length - allowedLength;
      break;
    case "end":
      startSliceEnd = allowedLength;
      endSliceStart = input.length;
      break;
    case "middle":
      const half = Math.floor(allowedLength / 2);
      startSliceEnd = half;
      endSliceStart = input.length - (allowedLength - half);
      break;
    default:
      throw new Error("Invalid position. Use 'start', 'end', or 'middle'.");
  }

  // Create the truncated string
  return (
    input.slice(0, startSliceEnd) + replacement + input.slice(endSliceStart)
  );
}