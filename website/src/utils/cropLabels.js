// Helpers for the offline model's PlantVillage labels, e.g. "Strawberry___Leaf_scorch"

const CROP_NAMES = {
  'apple': 'Apple',
  'blueberry': 'Blueberry',
  'cherry': 'Cherry',
  'corn': 'Corn (Maize)',
  'grape': 'Grape',
  'orange': 'Orange',
  'peach': 'Peach',
  'pepper': 'Bell Pepper',
  'potato': 'Potato',
  'raspberry': 'Raspberry',
  'soybean': 'Soybean',
  'squash': 'Squash',
  'strawberry': 'Strawberry',
  'tomato': 'Tomato'
};

// Lowercase and strip everything but letters/digits so differently spelled keys still match
export const normalizeLabel = (label = '') => label.toLowerCase().replace(/[^a-z0-9]/g, '');

// Works for raw labels ("Pepper,_bell___Bacterial_spot") and saved display text ("Pepper, bell Bacterial spot")
export const getCropFromLabel = (label = '') => {
  const firstWord = label.trim().split(/[^A-Za-z]/)[0].toLowerCase();
  return CROP_NAMES[firstWord] || null;
};

export const isHealthyLabel = (label = '') => /healthy/i.test(label);
