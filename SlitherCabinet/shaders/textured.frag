#version 330 core

in vec3 color;
in vec3 normal;
in vec3 frag_pos;
in vec3 view_pos;
in vec2 UV;

uniform sampler2D tex_front;
uniform sampler2D tex_back;

uniform int fbo_switcher;
uniform ivec3 object_color_identifier_default_fbo;
uniform ivec3 object_color_identifier_custom_fbo;
uniform ivec3 current_pixel_color;
uniform ivec4 highlight_colour = ivec4(1, 0, 0, 1);

out vec4 frag_color;

struct light
{
    vec3 position;
    vec3 color;
};

#define NUM_LIGHTS 3
uniform light light_data[NUM_LIGHTS];

vec4 Create_Light(vec3 light_pos, vec3 light_color, vec3 normal, vec3 frag_pos, vec3 view_dir)
{
    //ambient
    float a_strength = 1;
    vec3 ambient = a_strength * light_color;

    //diffuse
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - frag_pos);
    float diff = max(dot(norm, light_dir), 0);
    vec3 diffuse = diff * light_color;

    //specular
    float s_strength = 0.0;
    vec3 reflect_dir = normalize(-light_dir - norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular = s_strength * spec * light_color;

    return vec4(color * (ambient + diffuse + specular), 1);
}

void main()
{
    vec3 view_dir = normalize(view_pos - frag_pos);

    frag_color = Create_Light(light_data[0].position, light_data[0].color, normal, frag_pos, view_dir);
    frag_color += Create_Light(light_data[1].position, light_data[1].color, normal, frag_pos, view_dir);
    frag_color += Create_Light(light_data[2].position, light_data[2].color, normal, frag_pos, view_dir);

    if(fbo_switcher == 0)
    {
        if(object_color_identifier_default_fbo == current_pixel_color)
        {
            if (gl_FrontFacing)
            {
                frag_color = frag_color * texture(tex_front, UV)  * highlight_colour;
            }
            else // Fragment is back facing fragment
            {
                frag_color = frag_color * texture(tex_back, UV) *  highlight_colour;
            }
        }
        else
        {
            if (gl_FrontFacing)
            {
                frag_color = frag_color * texture(tex_front, UV);
            }
            else // Fragment is back facing fragment
            {
                frag_color = frag_color * texture(tex_back, UV);
            }
        }
    }
    else
    {
        frag_color = vec4(object_color_identifier_custom_fbo[0] / 255.0,
                          object_color_identifier_custom_fbo[1] / 255.0,
                          object_color_identifier_custom_fbo[2] / 255.0,
                                                                    1.0);
    }
}