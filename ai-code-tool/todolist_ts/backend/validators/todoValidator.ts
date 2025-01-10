import Joi from 'joi';

// Define the validation schema for the Todo model
export const todoValidationSchema = Joi.object({
  text: Joi.string().min(1).required().messages({
    'string.base': '"text" should be a type of "text"',
    'string.empty': '"text" cannot be an empty field',
    'any.required': '"text" is a required field',
  }),
});